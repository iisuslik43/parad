//
// Created by iisus on 22.08.2017.
//
#include "struct.h"

void save_gun(gun* g, FILE* file){
    fwrite (&g, sizeof(file),1, file );
}

void save_list(gun* head){
    FILE *file = fopen("for_guns","w");
    if(file == NULL){
        printf("Can`t find file for_guns");
        clear(head);
        exit(0);
    }
    while(head){
        save_gun(head, file);
        head = head->next;
    }
}

void load_gun(gun* g, FILE* file){
    fread (&g, sizeof(file),1, file );
}

void load_list(gun* head){
    FILE *file = fopen("for_guns","r");
    if(file == NULL){
        printf("Can`t find file for_guns");
        clear(head);
        exit(0);
    }
    while (!feof(file)){
        gun* g = malloc(sizeof(gun));
        load_gun(g, file);
    }

}

void clear(gun* head){
    while(head){
        gun* temp = head;
        head = head->next;
        free(temp);
    }
}
gun* add(gun* head, gun* new){
    if(!head){
        head = new;
        return head;
    }
    gun* temp = head;
    while(temp->next){
        temp = temp->next;
    }
    temp->next = new;
    new->prev = temp;
    return  head;
}



void delete(gun* del){
    if(del->prev)
        del->prev->next = del->next;
    if(del->next)
        del->next->prev = del->prev;
}

void insert(gun* what, gun* before_what){
    what->next = before_what;
    if(before_what->prev){
        before_what->prev->next = what;
    }
    what->prev = before_what->prev;
    before_what->prev = what;
}

int comp(gun* a, gun* b, int type_or_price){
    if(type_or_price == BY_TYPE){
        return -strcmp(a->type, b->type);
    }
    else{
        if(a->price < b-> price)
            return 1;
        if(a->price == b->price)
            return 0;
        else
            return -1;
    }
}

gun* sort(gun* head, int type_or_price){
    gun* now_head = head;
    int first_min = 1;
    while(now_head->next){
        gun* temp = now_head;
        gun* min = now_head;
        while(temp){
            if(comp(temp, min, type_or_price) == 1){
                min = temp;
            }
            temp = temp->next;
        }
        if(first_min){
            head = min;
            first_min = 0;
        }
        printf("%d\n", min->price);
        if(min == now_head) {
            now_head = now_head->next;
            continue;
        }

        delete(min);
        printf("fuck\n");
        insert(min, now_head);
        printf("fuck\n");
    }
    return head;
}


