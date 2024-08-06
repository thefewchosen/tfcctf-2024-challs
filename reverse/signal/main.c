#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <signal.h>
#include <sys/mman.h>

#define FLAG_INNER_LENGTH 32

void GenerateChallenge(char Challenge[FLAG_INNER_LENGTH]) {
    constexpr char alphabet[] = "abcdef0123456789";
    srand(time(NULL));
    for (int i = 0; i < FLAG_INNER_LENGTH; i++) {
        Challenge[i] = alphabet[rand() % (sizeof(alphabet) - 1)];
    }
}

#define HAS_INCLUDE(x) __has_include(x)
#define CHECK_INCLUDE(x) HAS_INCLUDE(x)

const char* gInput = nullptr;

#define CONCAT(x, y) x ## y
#define FLAG_CHAR(Index) CONCAT(FLAG_, Index)
#define CHECK_FLAG_CHAR(Index) do {\
    if (gInput[(Index)] != FLAG_CHAR(Index)) { \
        printf("Nope\n"); \
        exit(1); \
    } \
} while(0);

void HandleSigsegv(int) {
    CHECK_FLAG_CHAR(0);
    CHECK_FLAG_CHAR(1);
    CHECK_FLAG_CHAR(2);
    CHECK_FLAG_CHAR(3);
    CHECK_FLAG_CHAR(4);
    __builtin_trap();
    exit(0);
}

void HandleSigtrap(int) {
    CHECK_FLAG_CHAR(5);
    CHECK_FLAG_CHAR(6);
    CHECK_FLAG_CHAR(7);
    CHECK_FLAG_CHAR(8);
    CHECK_FLAG_CHAR(9);
    asm volatile (
#if defined(__aarch64__)
        "udf #1337"
#elif defined(__x86_64__)
        "ud2"
#else
# error "Invalid architecture"
#endif
    );
    exit(0);
}

void HandleSigill(int) {
    CHECK_FLAG_CHAR(10);
    CHECK_FLAG_CHAR(11);
    CHECK_FLAG_CHAR(12);
    CHECK_FLAG_CHAR(13);
    CHECK_FLAG_CHAR(14);
    alarm(2);
    pause();
    exit(0);
}

void HandleSigalrm(int) {
    CHECK_FLAG_CHAR(15);
    CHECK_FLAG_CHAR(16);
    CHECK_FLAG_CHAR(17);
    CHECK_FLAG_CHAR(18);
    CHECK_FLAG_CHAR(19);
    int pipeFds[2];
    pipe(pipeFds);
    close(pipeFds[0]);
    char output[1];
    write(pipeFds[1], &output[0], 1);
    exit(0);
}

void HandleSigpipe(int) {
    CHECK_FLAG_CHAR(20);
    CHECK_FLAG_CHAR(21);
    CHECK_FLAG_CHAR(22);
    CHECK_FLAG_CHAR(23);
    CHECK_FLAG_CHAR(24);
    abort();
    exit(0);
}

void HandleSigabrt(int) {
    CHECK_FLAG_CHAR(25);
    CHECK_FLAG_CHAR(26);
    CHECK_FLAG_CHAR(27);
    CHECK_FLAG_CHAR(28);
    CHECK_FLAG_CHAR(29);
    CHECK_FLAG_CHAR(30);
    CHECK_FLAG_CHAR(31);
    printf("Correct!\n");
    exit(0);
}

void (*gHandlers[32])(int) = {
    [SIGSEGV] = HandleSigsegv,
    [SIGTRAP] = HandleSigtrap,
    [SIGILL] = HandleSigill,
    [SIGALRM] = HandleSigalrm,
    [SIGPIPE] = HandleSigpipe,
    [SIGABRT] = HandleSigabrt,
};

#define ARRAYSIZE(Array) (sizeof((Array)) / sizeof((Array)[0]))

int main(const int argc, char* const* argv) {
#if CHECK_INCLUDE(FLAG_FILE)
    if (argc != 2) {
        printf("?\n");
        exit(-1);
    }
    gInput = argv[1];
    for (int i = 0; i < ARRAYSIZE(gHandlers); i++) {
        if (gHandlers[i] == nullptr) {
            continue;
        }
        struct sigaction action = {
            .sa_handler = gHandlers[i],
            .sa_flags = SA_RESTART,
            .sa_mask = 0,
        };
        sigaction(i, &action, nullptr);
    }
    *((volatile char *)0x1337) = 0;
#else
    char challenge[FLAG_INNER_LENGTH] = { 0 };
    GenerateChallenge(&challenge[0]);
    printf("Generated challenge %s\n", challenge);
    FILE* flag = fopen(FLAG_FILE, "w");
    fwrite(challenge, 1, FLAG_INNER_LENGTH, flag);
    fclose(flag);
    printf("Run again to generate full executable\n");
    exit(0);
#endif
}

