/*
 * hns_run : lanceur mGBA sans interface, piloté par script.
 *
 * Usage :
 *   hns_run --rom ROM --sav FICHIER.sav [--out DOSSIER] [--states DOSSIER]
 *           [--x2] [--fresh] [--prefix N] script.txt [script2.txt ...]
 *   (un script "-" lit l'entrée standard)
 *
 * Commandes de script (une par ligne, '#' = commentaire) :
 *   wait N                 avance N images sans touche
 *   press KEY [H] [W]      appuie KEY pendant H images (déf. 4) puis relâche W images (déf. 16)
 *                          KEY peut combiner des touches : A+B, START, UP+B...
 *   hold KEY N             maintient KEY pendant N images (puis relâche)
 *   repeat N CMD...        répète N fois la commande CMD (ex. : repeat 10 press A)
 *   shot NOM               capture PNG <out>/NN_NOM.png (NN = compteur automatique)
 *   save FICHIER           sauvegarde un état (relatif à --states)
 *   load FICHIER           charge un état (relatif à --states)
 *   rtc AAAA-MM-JJTHH:MM   fixe l'horloge de la cartouche (avance ensuite avec l'émulation)
 *   reset                  redémarre la console
 *   include FICHIER        exécute un autre script (relatif au script courant)
 *   echo TEXTE             affiche TEXTE sur la sortie standard
 *   peek ADRESSE [N]       affiche N octets (déf. 16) à l'adresse (hexadécimale) du bus GBA
 *   counter N              force le compteur de captures à N
 *
 * Touches : A B SELECT START RIGHT LEFT UP DOWN R L
 */
#define _DEFAULT_SOURCE
#define _DARWIN_C_SOURCE
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba/core/serialize.h>
#include <mgba/core/interface.h>
#include <mgba-util/png-io.h>
#include <mgba-util/vfs.h>

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>
#include <libgen.h>

#define W 240
#define H 160

static struct mCore* core;
static color_t* video;
static const char* outDir = ".";
static const char* stateDir = ".";
static int doX2 = 0;
static int shotCounter = 1;
static unsigned long long totalFrames = 0;
static int errors = 0;

/* ---- journalisation : on n'affiche que les erreurs ---- */
static void logCb(struct mLogger* l, int cat, enum mLogLevel level, const char* fmt, va_list args) {
	(void) l;
	(void) cat;
	if (level & (mLOG_FATAL | mLOG_ERROR)) {
		fprintf(stderr, "[mgba] ");
		vfprintf(stderr, fmt, args);
		fprintf(stderr, "\n");
	}
}
static struct mLogger logger = { .log = logCb };

static void runFrames(int n, uint32_t keys) {
	core->setKeys(core, keys);
	for (int i = 0; i < n; ++i) {
		core->runFrame(core);
		++totalFrames;
	}
	core->setKeys(core, 0);
}

static int keyBit(const char* name) {
	static const char* names[] = { "A", "B", "SELECT", "START", "RIGHT", "LEFT", "UP", "DOWN", "R", "L" };
	for (int i = 0; i < 10; ++i) {
		if (!strcasecmp(name, names[i])) {
			return i;
		}
	}
	return -1;
}

static int parseKeys(const char* spec, uint32_t* out) {
	char buf[128];
	snprintf(buf, sizeof(buf), "%s", spec);
	uint32_t keys = 0;
	char* save = NULL;
	for (char* tok = strtok_r(buf, "+", &save); tok; tok = strtok_r(NULL, "+", &save)) {
		int b = keyBit(tok);
		if (b < 0) {
			return 0;
		}
		keys |= 1u << b;
	}
	*out = keys;
	return 1;
}

static int mkdirs(const char* path) {
	char tmp[1024];
	snprintf(tmp, sizeof(tmp), "%s", path);
	for (char* p = tmp + 1; *p; ++p) {
		if (*p == '/') {
			*p = 0;
			mkdir(tmp, 0755);
			*p = '/';
		}
	}
	return mkdir(tmp, 0755) == 0 || errno == EEXIST;
}

static int writePng(const char* path, int scale) {
	struct VFile* vf = VFileOpen(path, O_CREAT | O_TRUNC | O_WRONLY);
	if (!vf) {
		return 0;
	}
	png_structp png = PNGWriteOpen(vf);
	png_infop info = PNGWriteHeader(png, W * scale, H * scale);
	int ok;
	if (scale == 1) {
		ok = PNGWritePixels(png, W, H, W, video);
	} else {
		color_t* big = malloc(sizeof(color_t) * W * H * scale * scale);
		for (int y = 0; y < H * scale; ++y) {
			for (int x = 0; x < W * scale; ++x) {
				big[y * W * scale + x] = video[(y / scale) * W + x / scale];
			}
		}
		ok = PNGWritePixels(png, W * scale, H * scale, W * scale, big);
		free(big);
	}
	PNGWriteClose(png, info);
	vf->close(vf);
	return ok;
}

static void joinPath(char* out, size_t n, const char* dir, const char* file) {
	if (file[0] == '/') {
		snprintf(out, n, "%s", file);
	} else {
		snprintf(out, n, "%s/%s", dir, file);
	}
}

static int setRtc(const char* iso) {
	struct tm tm;
	memset(&tm, 0, sizeof(tm));
	int y, mo, d, h = 0, mi = 0, s = 0;
	if (sscanf(iso, "%d-%d-%dT%d:%d:%d", &y, &mo, &d, &h, &mi, &s) < 3) {
		return 0;
	}
	tm.tm_year = y - 1900;
	tm.tm_mon = mo - 1;
	tm.tm_mday = d;
	tm.tm_hour = h;
	tm.tm_min = mi;
	tm.tm_sec = s;
	time_t t = timegm(&tm);
	core->rtc.override = RTC_FAKE_EPOCH;
	core->rtc.value = (int64_t) t * 1000;
	return 1;
}

static int runScript(const char* path, int depth);

static int execLine(char* line, const char* scriptDir, const char* where, int depth) {
	char* argv[16];
	int argc = 0;
	char* save = NULL;
	char* rest = NULL;
	/* echo : on garde le reste de la ligne tel quel */
	while (*line == ' ' || *line == '\t') {
		++line;
	}
	if (!strncmp(line, "echo", 4) && (line[4] == ' ' || line[4] == 0)) {
		printf("%s\n", line[4] ? line + 5 : "");
		fflush(stdout);
		return 1;
	}
	for (char* tok = strtok_r(line, " \t", &save); tok && argc < 16; tok = strtok_r(NULL, " \t", &save)) {
		argv[argc++] = tok;
	}
	(void) rest;
	if (!argc) {
		return 1;
	}
	const char* cmd = argv[0];
	if (!strcmp(cmd, "wait") && argc >= 2) {
		runFrames(atoi(argv[1]), 0);
	} else if (!strcmp(cmd, "press") && argc >= 2) {
		uint32_t keys;
		if (!parseKeys(argv[1], &keys)) {
			goto bad;
		}
		int h = argc >= 3 ? atoi(argv[2]) : 4;
		int w = argc >= 4 ? atoi(argv[3]) : 16;
		runFrames(h, keys);
		runFrames(w, 0);
	} else if (!strcmp(cmd, "hold") && argc >= 3) {
		uint32_t keys;
		if (!parseKeys(argv[1], &keys)) {
			goto bad;
		}
		runFrames(atoi(argv[2]), keys);
	} else if (!strcmp(cmd, "repeat") && argc >= 3) {
		int n = atoi(argv[1]);
		char sub[512];
		for (int i = 0; i < n; ++i) {
			sub[0] = 0;
			for (int j = 2; j < argc; ++j) {
				strlcat(sub, argv[j], sizeof(sub));
				strlcat(sub, " ", sizeof(sub));
			}
			if (!execLine(sub, scriptDir, where, depth)) {
				return 0;
			}
		}
	} else if (!strcmp(cmd, "shot") && argc >= 2) {
		char path[1024];
		mkdirs(outDir);
		snprintf(path, sizeof(path), "%s/%02d_%s.png", outDir, shotCounter, argv[1]);
		if (!writePng(path, 1)) {
			fprintf(stderr, "%s : échec de la capture %s\n", where, path);
			++errors;
		}
		if (doX2) {
			char dir2[1024];
			snprintf(dir2, sizeof(dir2), "%s/x2", outDir);
			mkdirs(dir2);
			snprintf(path, sizeof(path), "%s/%02d_%s.png", dir2, shotCounter, argv[1]);
			writePng(path, 2);
		}
		++shotCounter;
	} else if (!strcmp(cmd, "counter") && argc >= 2) {
		shotCounter = atoi(argv[1]);
	} else if (!strcmp(cmd, "save") && argc >= 2) {
		char path[1024];
		joinPath(path, sizeof(path), stateDir, argv[1]);
		mkdirs(stateDir);
		struct VFile* vf = VFileOpen(path, O_CREAT | O_TRUNC | O_RDWR);
		if (!vf || !mCoreSaveStateNamed(core, vf, SAVESTATE_SAVEDATA | SAVESTATE_RTC)) {
			fprintf(stderr, "%s : échec de la sauvegarde d'état %s\n", where, path);
			++errors;
		}
		if (vf) {
			vf->close(vf);
		}
	} else if (!strcmp(cmd, "load") && argc >= 2) {
		char path[1024];
		joinPath(path, sizeof(path), stateDir, argv[1]);
		struct VFile* vf = VFileOpen(path, O_RDONLY);
		if (!vf || !mCoreLoadStateNamed(core, vf, SAVESTATE_SAVEDATA | SAVESTATE_RTC)) {
			fprintf(stderr, "%s : échec du chargement d'état %s\n", where, path);
			if (vf) {
				vf->close(vf);
			}
			return 0;
		}
		vf->close(vf);
	} else if (!strcmp(cmd, "rtc") && argc >= 2) {
		if (!setRtc(argv[1])) {
			goto bad;
		}
	} else if (!strcmp(cmd, "reset")) {
		core->reset(core);
	} else if (!strcmp(cmd, "include") && argc >= 2) {
		char path[1024];
		joinPath(path, sizeof(path), scriptDir, argv[1]);
		return runScript(path, depth + 1);
	} else if (!strcmp(cmd, "peek") && argc >= 2) {
		uint32_t addr = strtoul(argv[1], NULL, 16);
		int n = argc >= 3 ? atoi(argv[2]) : 16;
		printf("%08X:", addr);
		for (int i = 0; i < n; ++i) {
			printf(" %02X", core->rawRead8(core, addr + i, -1));
		}
		printf("\n");
		fflush(stdout);
	} else {
		goto bad;
	}
	return 1;
bad:
	fprintf(stderr, "%s : commande invalide « %s »\n", where, cmd);
	++errors;
	return 1;
}

static int runScript(const char* path, int depth) {
	if (depth > 16) {
		fprintf(stderr, "include trop profond : %s\n", path);
		return 0;
	}
	FILE* f = strcmp(path, "-") ? fopen(path, "r") : stdin;
	if (!f) {
		fprintf(stderr, "script introuvable : %s\n", path);
		return 0;
	}
	char dirbuf[1024];
	snprintf(dirbuf, sizeof(dirbuf), "%s", strcmp(path, "-") ? path : "./x");
	char* scriptDir = dirname(dirbuf);
	char dirCopy[1024];
	snprintf(dirCopy, sizeof(dirCopy), "%s", scriptDir);
	char line[1024];
	int lineno = 0;
	int ok = 1;
	while (fgets(line, sizeof(line), f)) {
		++lineno;
		char* hash = strchr(line, '#');
		if (hash && strncmp(line, "echo", 4)) {
			*hash = 0;
		}
		line[strcspn(line, "\r\n")] = 0;
		char where[1200];
		snprintf(where, sizeof(where), "%s:%d", path, lineno);
		if (!execLine(line, dirCopy, where, depth)) {
			ok = 0;
			break;
		}
	}
	if (f != stdin) {
		fclose(f);
	}
	return ok;
}

static void usage(void) {
	fprintf(stderr,
	        "usage : hns_run --rom ROM --sav FICHIER.sav [--out DOSSIER] [--states DOSSIER]\n"
	        "                [--x2] [--fresh] script.txt [...]\n");
}

int main(int argc, char** argv) {
	const char* rom = NULL;
	const char* sav = NULL;
	int fresh = 0;
	int first = argc;
	for (int i = 1; i < argc; ++i) {
		if (!strcmp(argv[i], "--rom") && i + 1 < argc) {
			rom = argv[++i];
		} else if (!strcmp(argv[i], "--sav") && i + 1 < argc) {
			sav = argv[++i];
		} else if (!strcmp(argv[i], "--out") && i + 1 < argc) {
			outDir = argv[++i];
		} else if (!strcmp(argv[i], "--states") && i + 1 < argc) {
			stateDir = argv[++i];
		} else if (!strcmp(argv[i], "--x2")) {
			doX2 = 1;
		} else if (!strcmp(argv[i], "--fresh")) {
			fresh = 1;
		} else if (!strcmp(argv[i], "-h") || !strcmp(argv[i], "--help")) {
			usage();
			return 0;
		} else {
			first = i;
			break;
		}
	}
	if (!rom || !sav || first >= argc) {
		usage();
		return 2;
	}
	mLogSetDefaultLogger(&logger);

	core = mCoreFind(rom);
	if (!core || !core->init(core)) {
		fprintf(stderr, "impossible d'initialiser le cœur pour %s\n", rom);
		return 1;
	}
	mCoreInitConfig(core, NULL);
	struct mCoreOptions opts = { .useBios = false, .skipBios = true, .volume = 0x100 };
	mCoreConfigLoadDefaults(&core->config, &opts);
	mCoreLoadForeignConfig(core, &core->config); /* ne lit pas la config utilisateur */

	unsigned w, h;
	core->desiredVideoDimensions(core, &w, &h);
	if (w != W || h != H) {
		fprintf(stderr, "dimensions inattendues %ux%u\n", w, h);
	}
	video = calloc(W * H, sizeof(color_t));
	core->setVideoBuffer(core, video, W);

	if (!mCoreLoadFile(core, rom)) {
		fprintf(stderr, "impossible de charger la ROM %s\n", rom);
		return 1;
	}
	if (fresh) {
		unlink(sav);
	}
	struct VFile* savf = VFileOpen(sav, O_CREAT | O_RDWR);
	if (!savf || !core->loadSave(core, savf)) {
		fprintf(stderr, "impossible d'ouvrir la sauvegarde %s\n", sav);
		return 1;
	}
	core->reset(core);

	struct timespec t0, t1;
	clock_gettime(CLOCK_MONOTONIC, &t0);
	int ok = 1;
	for (int i = first; i < argc && ok; ++i) {
		ok = runScript(argv[i], 0);
	}
	clock_gettime(CLOCK_MONOTONIC, &t1);
	double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;
	fprintf(stderr, "[hns_run] %llu images en %.2f s (%.0f images/s, x%.1f temps réel)\n", totalFrames, secs,
	        secs > 0 ? totalFrames / secs : 0, secs > 0 ? totalFrames / secs / 59.7275 : 0);

	core->deinit(core);
	free(video);
	return (ok && !errors) ? 0 : 1;
}
