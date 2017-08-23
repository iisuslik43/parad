//
// Created by iisus on 23.08.2017.
//

#ifndef KUR_STRUCT_H
#define KUR_STRUCT_H
#include <memory.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
static const int BY_PRICE = 1;
static const int BY_TYPE = -1;

typedef struct gun gun;
struct gun{
    char type[20];
    int ammo, caliber, price;
    gun* prev;
    gun* next;
};

void save_gun(gun* g, FILE* file);
void save_list(gun* head);

void clear(gun* head);
gun* add(gun* head, gun* new);
int comp(gun* a, gun* b, int type_or_price);
gun* sort(gun* head, int type_or_price);
#endif //KUR_STRUCT_H
