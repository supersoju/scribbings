#include "linked.h"


int main(int argc, char *argv[])
{
    int num1 = 1;
    int num2 = 2;
    int num3 = 3;
    struct node* head = NULL;
    insert(&head, num1);
    insert(&head, num2);
    insert(&head, num3);
    display(head);
    delete(&head, num3);
    display(head);
    // Circular List
    printf("Circular List\n");
    struct cnode* chead =NULL;
    cinsert(&chead, num1);
    cinsert(&chead, num2);
    cinsert(&chead, num3);
    cdisplay(chead);
    cdelete(&chead, num1);
    cdisplay(chead);

    return 0;
}
