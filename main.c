
#include "view.h"
int main() {
    printf("Hello, World!\n");
    gun* head = NULL;

    gun* new_gun;

    for(int i = 0; i < 4; i++){
        new_gun =  get_gun();
        head = add(head, new_gun);
    }
    head = sort(head, BY_TYPE);
    print_list(head);
    clear(head);
    return 0;
}