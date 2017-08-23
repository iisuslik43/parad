//
// Created by iisus on 23.08.2017.
//

#include "view.h"

void print_gun(gun* g){
    printf("%s %d %d %d\n", g->type, g->ammo, g->caliber, g->price);
}

void print_list(gun* head){
    while(head){
        print_gun(head);
        head = head->next;
    }
}

gun* get_gun(){
    gun* new = malloc(sizeof(gun));
    new->next = new->prev = NULL;
    printf("Write type:\n");
    scanf("%s", new->type);
    /*printf("Write ammo:\n");
    scanf("%d", &new->ammo);
    printf("Write caliber:\n");
    scanf("%d", &new->caliber);
    printf("Write price:\n");
    scanf("%d", &new->price);*/
    return new;
}
void print_less(gun* head, int cost){
    while(head){
        if(head->price <= cost)
            print_gun(head);
        head = head->next;
    }
}