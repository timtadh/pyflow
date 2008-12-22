int printf;
char getchar;
int EOF = -1;

int main()
{
    short int c, n1;
    
    n1 = 0;
    while ((c = getchar()) != EOF)
    {
        if (c == '\n')
        {
            n1 += 1;
        }
    }
    printf("Number of Lines: %d\n", n1); 
}

int sub()
{
    int x;
}