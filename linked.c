#include<stdio.h>
#include<stdlib.h>

struct node
{
    int data;
    struct node* next;
};

struct cnode
{
    int data;
    struct cnode* right;
    struct cnode* left;
};

void cinsert(struct cnode** head, int d)
{
    struct cnode* curr = malloc(sizeof(struct cnode));
    curr->data = d;
    curr->right = NULL;
    curr->left = NULL;

    if(*head ==NULL)
    {
        *head = curr;
        return;
    }
    if ((*head)->left == NULL)
    {
        (*head)->left = curr;
        (*head)->right = curr;
        curr->left = *head;
        curr->right = *head;
        return;
    }
    struct cnode* temp = (*head)->left;
    temp->right = curr;
    curr->left = temp;
    curr->right = *head;
    (*head)->left = curr;
}

void insert(struct node** head, int d)
{    
    struct node* curr = malloc(sizeof(struct node));
    curr->data = d;
    curr->next = NULL;
    if(*head == NULL)
    {
        *head = curr;
        return;
    }
    curr->next=(*head);
    *head = curr;
    return;
}


void cdelete(struct cnode** head, int d)
{
    if(*head ==NULL)
    {
        printf("No data to delete\n");
        return;
    }
    struct cnode *current = *head;

    if ((*head)->data == d)
    {
        (current->left)->right = current->right;
        (current->right)->left = current->left;
        *head = current->right;
        free(current);
        return;
    }

    while(current->right != *head)
    {
        if(current->data == d)
            break;
        current = current->right;
    }
    (current->left)->right = current->right;
    (current->right)->left = current->left;
    free(current);
    return;
}




void delete(struct node** head, int d)
{
    if(*head == NULL)
    {
        printf("No data to delete\n");
        return;
    }

    struct node* current = *head;
    struct node* prev;
    while(current!=NULL) 
    {
        if(current->data == d)
            break;
        prev = current;
        current = current->next;
    }
    if(current==NULL)
    {
        printf("No entry found\n");
        return;
    }
    else if(current->next==NULL)
    {
        free(current);
        prev->next = NULL;
    }
    else if(current == *head)
    {
        *head = (*head)->next;
        free(current);
    }
    else
    {
        prev->next = current->next;
        free(current);
    }
    return;
}

    
void display(struct node* head)
{
    printf("In Display\n");
    if(head == NULL)
    {
        printf("No data\n");
        return;    
    }
    struct node* current = head;
    while(current !=NULL)
    {
        printf("%d\n", current->data);
        current = current->next;
    }
} 

void cdisplay(struct cnode* head)
{
    printf("In Circular Display\n");
    if(head == NULL)
    {
        printf("No data\n");
        return;
    }
    struct cnode* current = head;
    do{
        current = current->right;
        printf("%d\n", current->data);
    }while(current != head);
}

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
