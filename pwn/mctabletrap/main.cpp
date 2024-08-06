#include <iostream>
#include <fstream>
#include <vector>
#include <string.h>
#include <unistd.h>
#include <random>

// TO DO: modify read_stdin func because it crashes when you try to do the stdout leak
// Maybe do not read description of the bug and just read an int or something

void read_stdin(char *buf, int size) {
    while (std::cin.peek() == '\n') {
        std::cin.ignore();
    }
    std::cin.getline(buf, size - 1);
    // std::cout << "[*] Read: " << buf << std::endl;
    buf[size - 1] = '\0';
}

class User {
public:
    char stats[16];
    int id;
    char username[64];
    char password[64];
    char email[64];
    int points;
    bool used_change;
    int has_reported;

    User() {
        used_change = false;
        points = 0;
        has_reported = 0;
    }
    

    virtual void print_data() {
        std::cout << "ID: " << id << std::endl;
        std::cout << "Username: " << username << std::endl;
        std::cout << "Email: " << email << std::endl;
    }

    virtual void change_password() {
        std::cout << "[?] Enter new password: ";
        read_stdin(password, 64);
    }

    void change_stat(int index, char value) {
        if (used_change) {
            std::cout << "[!] You have already used your change!" << std::endl;
            return;
        }
        stats[index - 1] = value;
        used_change = true;
    }

    void print_stats() {
        std::cout << "--- Stats ---" << std::endl;
        std::cout << "[ ";
        for (int i = 0; i < 16; i++) {
            std::cout << stats[i] << " ";
        }
        std::cout << "]" << std::endl;
    }
};

std::vector<User *> users;

class Admin : public User {
public:
    void print_data() override {
        std::cout << "Superuser: true" << std::endl;
        std::cout << "ID: " << id << std::endl;
        std::cout << "Username: " << username << std::endl;
        std::cout << "Email: " << email << std::endl;
    }
    void change_password() override {
        std::cout << "[!] You are an admin so you can change anyone's password!" << std::endl;
        std::cout << "[?] Enter the user's ID: ";
        int id;
        std::cin >> id;
        for (int i = 0; i < users.size(); i++) {
            if (users[i]->id == id) {
                std::cout << "[!] User found!" << std::endl;
                std::cout << "[!] Enter new password: ";
                read_stdin(users[i]->password, 64);
                return;
            }
        }
    }
};

void load_users() {
    std::ifstream file("db.txt");
    if (file.is_open()) {
        int id_buf, points_buf;
        char username_buf[64], password_buf[64], email_buf[64];

        while (file >> id_buf >> username_buf >> password_buf >> email_buf >> points_buf) {
            if (!strcmp(username_buf, "admin")) {
                Admin *admin = new Admin();
                admin->id = id_buf;
                admin->points = points_buf;
                strcpy(admin->username, username_buf);
                strcpy(admin->password, password_buf);
                strcpy(admin->email, email_buf);
                users.push_back(admin);
            } else {
                User *user = new User();
                user->id = id_buf;
                user->points = points_buf;
                strcpy(user->username, username_buf);
                strcpy(user->password, password_buf);
                strcpy(user->email, email_buf);
                users.push_back(user);
            }
        }
    }
}

void save_users() {
    std::ofstream file("db.txt");
    if (file.is_open()) {
        for (int i = 0; i < users.size(); i++) {
            file << users[i]->id << " " << users[i]->username << " " << users[i]->password << " " << users[i]->email << " " << users[i]->points << std::endl;
        }
    }
}

void typewriter(const char *str) {
    for (int i = 0; i < strlen(str); i++) {
        std::cout << str[i];
        std::cout.flush();
        usleep(10000);
    }
    std::cout << std::endl;
}

struct BUG {
    char *title;
    char *description;
    char *type;
} bugs[8];

BUG *bug_report = &bugs[0];
char game_coeffs[16];

void play(User *user) {
    std::cout << std::endl;

    typewriter("----????????????============[+]============????????????----");
    typewriter("[!] Here is how the game works:");
    typewriter("[+] Each player has a stats array of 16 elements.");
    typewriter("[+] Each element can be a number between 0 and 256.");
    typewriter("[+] The game master has a coeffiecient array for each element which is initially random and");
    typewriter("    TOTALLY NOT RIGGED or modifyable.");
    typewriter("[+] All of your stats are multiplied by the game master's coefficients and the result is your");
    typewriter("    magic number.");
    typewriter("[+] A new random number is generated and if your magic number modulo 256 is greater");
    typewriter("    than the random number you win!");
    typewriter("----????????????============[+]============????????????----");
    std::cout << "[ ";
    int *rand_idx = new int[4];
    for (int i = 0; i < 4; i++) {
        rand_idx[i] = rand() % 16;
    }
    for (int i = 0; i < 16; i++) {
        if (i == rand_idx[0] || i == rand_idx[1] || i == rand_idx[2] || i == rand_idx[3]) {
            std::cout << game_coeffs[i] << " ";
        } else {
            std::cout << "? ";
        }
    }
    std::cout << "]" << std::endl;
    delete[] rand_idx;

    std::cout << "[???] Calculating [";
    for (int i = 0; i < 10; i++) {
        std::cout << "=";
        std::cout.flush();
        usleep(300000);
    }
    std::cout << "] Done!" << std::endl;
    int magic_number = 0;
    for (int i = 0; i < 16; i++) {
        magic_number += user->stats[i] * game_coeffs[i];
    }
    magic_number %= 256;

    int random_number = rand() % 256;
    std::cout << "[*] Your magic number is: " << magic_number << std::endl;
    std::cout << "[*] Random number is: " << random_number << std::endl;
    if (magic_number % 256 > random_number) {
        std::cout << "[*] You won!" << std::endl;
        user->points += 10;
    } else {
        std::cout << "[*] You lost!" << std::endl;
        user->points -= 10;
    }

}

void print_users() {
    std::cout << "--- Users ---" << std::endl;
    for (int i = 0; i < users.size(); i++) {
        users[i]->print_data();
        std::cout << "--- [++] ---" << std::endl;
    }
}

void print_inp() {
    std::cout << "[?] > ";
}

void print_welcome_menu() {
    std::cout << "--- Welcome to the totally not rigged game! ---" << std::endl;
    std::cout << "[1] Login" << std::endl;
    std::cout << "[2] Register" << std::endl;
}

void print_game_menu() {
    std::cout << "--- Game Menu ---" << std::endl;
    std::cout << "[1] Play" << std::endl;
    std::cout << "[2] Print stats" << std::endl;
    std::cout << "[3] Edit stats" << std::endl;
    std::cout << "[4] Report bug" << std::endl;
    std::cout << "[5] Change password" << std::endl;
    std::cout << "[6] Logout" << std::endl;
}

void print_admin_menu() {
    std::cout << "--- Admin Menu ---" << std::endl;
    std::cout << "[1] Print users" << std::endl;
    std::cout << "[2] Change user password" << std::endl;
    std::cout << "[3] Change game coefficients" << std::endl;
    std::cout << "[4] Read report" << std::endl;
    std::cout << "[5] Logout" << std::endl;
}

User *crt_User = nullptr;

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    srand(time(NULL));    
    load_users();

    for (int i = 0; i < 8; i++) {
        bugs[i].title = new char[512];
        bugs[i].description = new char[512];
        bugs[i].type = new char[64];
    }

    bugs[0].type = "UAF";
    bugs[1].type = "Heap Overflow";
    bugs[2].type = "Stack Overflow";
    bugs[3].type = "Integer Overflow";
    bugs[4].type = "Integer Underflow";
    bugs[5].type = "Use After Free";
    bugs[6].type = "Double Free";
    bugs[7].type = "Memory Leak";


    for (int i = 0; i < 16; i++) {
        game_coeffs[i] = rand() % 256;
    }
}

int main() {
    init();
start:
    print_welcome_menu();

    char *username_buf = new char[64];
    char *password_buf = new char[64];
    while (crt_User == nullptr) {
        print_inp();
        int choice;
        std::cin >> choice;
        switch (choice) {
            case 1:
                std::cout << "\n[?] Enter username: ";
                read_stdin(username_buf, 64);
                std::cout << "[?] Enter password: ";
                read_stdin(password_buf, 64);

                for (int i = 0; i < users.size(); i++) {
                    if (!strcmp(users[i]->username, username_buf) && !strcmp(users[i]->password, password_buf)) {
                        crt_User = users[i];
                        break;
                    } 
                }
                if (crt_User == nullptr) {
                    std::cout << "[!] Invalid credentials!" << std::endl;
                }
                break;
            case 2:
                std::cout << "\n[!] Registering is disabled for safety reasons!" << std::endl;
                break;
            case 3:
                exit(0);
            default:
                std::cout << "[!] Invalid choice!" << std::endl;
                break;
        }
    }

    std::cout << std::endl << "[*] Welcome " << crt_User->username << "!" << std::endl;
    std::cout << "[*] You have " << crt_User->points << " points!" << std::endl;
    std::cout << "[*] Your stats have been randomly generated!" << std::endl << std::endl;
    for (int i = 0; i < 16; i++) {
        crt_User->stats[i] = rand() % 256;
    }
    
    int choice;
    int index;
    int value;
    int maxi = 0;
    crt_User->used_change = false;
    if (crt_User->id != 1) {
        while (true) {
            print_game_menu();
            print_inp();
            std::cin >> choice;
            switch (choice) {
                case 1:
                    play(crt_User);
                    break;
                case 2:
                    crt_User->print_stats();
                    break;
                case 3:
                    std::cout << "[!] You may change at most 1 stat! Is this going to be your lucky number?" << std::endl;
                    std::cout << "[?] Enter the stat index(1 to 16): ";
                    std::cin >> index;
                    if (index > 16) {
                        std::cout << "[!] Invalid index!" << std::endl;
                        break;
                    }
                    std::cout << "[?] Enter the new value: ";
                    std::cin >> value;
                    crt_User->change_stat(index, value);
                    break;
                case 4:
                    if (crt_User->has_reported >= 2) {
                        std::cout << "[!] You have reported too many bugs!" << std::endl;
                        break;
                    }
                    crt_User->has_reported++;
                    std::cout << "[?] Choose a bug to report from the list below:" << std::endl;

                    maxi = 0;
                    for (int i = 0; i <= 8; i++) {
                        if (strlen(bugs[i].type) == 0)
                            break;
                        std::cout << "[" << i + 1 << "] " << bugs[i].type << std::endl;
                        maxi = i;
                    }
                    std::cout << "[?] Enter the bug index: ";
                    std::cin >> index;
                    if (!(index >= 0 && index <= maxi)) {
                        std::cout << "[!] Invalid index!" << std::endl;
                        break;
                    }
                    std::cout << "[!] Please detail the bug!" << std::endl;
                    std::cout << "[?] Title: ";
                    read_stdin(bug_report->title, 512);
                    break;
                case 5:
                    crt_User->change_password();
                    break;
                case 6:
                    crt_User = nullptr;
                    save_users();
                    goto start;

                default:
                    std::cout << "[!] Invalid choice!" << std::endl;
                    break;
            }
        }
    } else {
        int coeff_ch = 0;
        while (true) {
            print_admin_menu();
            print_inp();
            std::cin >> choice;
            switch (choice) {
                case 1:
                    print_users();
                    break;
                case 2:
                    crt_User->change_password();
                    break;
                case 3:
                    if (coeff_ch >= 2) {
                        std::cout << "[!] You have changed the coefficients too many times!" << std::endl;
                        break;
                    }
                    coeff_ch++;
                    std::cout << "[!] You may change at most 2 coefficients!" << std::endl;
                    std::cout << "[?] Enter the coefficient index(1 to 16): ";
                    std::cin >> index;
                    if (index > 16) {
                        std::cout << "[!] Invalid index!" << std::endl;
                        break;
                    }
                    std::cout << "[?] Enter the new value: ";
                    std::cin >> value;
                    game_coeffs[index - 1] = value;
                    break;
                case 4:
                    std::cout << "[!] Who cares about bugs when you have pancakes to eat?" << std::endl;
                    break;
                case 5:
                    crt_User = nullptr;
                    save_users();
                    goto start;
                default:
                    std::cout << "[!] Invalid choice!" << std::endl;
                    break;

            }
        }
    }
    return 0;
}