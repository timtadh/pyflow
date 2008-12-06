/*******************************************************************************
*
* FILE:     tbird.c
*
* DESC:     EECS 337 Homework Assignment 13
*
* AUTHOR:   caseid
*
* DATE:     November 25, 2008
*
* EDIT HISTORY: 
*
*   tbird tail lights are defined using 3 bits per side
*   0000 0000 all off
*   0111 1110 hazard on
*   0000 1000 right on 1
*   0000 1100 right on 2
*   0000 1110 right on 3
*   0001 0000 left on 1
*   0011 0000 left on 2
*   0111 0000 left on 3
*******************************************************************************/
char    lights = 0;
char    index;
char    count;

delay()
{
    index = 255;
    while( index)
    {
        index = index - 1;
        count = 255;
        while( count)
            count = count - 1;
    }
}

left()
{
    lights = 0x10;
    printf( "%d\n", lights);
    delay();
    lights = 0x30;
    printf( "%d\n", lights);
    delay();
    lights = 0x70;
    printf( "%d\n", lights);
    delay();
    lights = 0x00;
    printf( "%d\n", lights);
    delay();
    return;
}

right()
{
    lights = 0x08;
    printf( "%d\n", lights);
    delay();
    lights = 0x0c;
    printf( "%d\n", lights);
    delay();
    lights = 0x0e;
    printf( "%d\n", lights);
    delay();
    lights = 0x00;
    printf( "%d\n", lights);
    delay();
    return;
}

hazard()
{
    lights = 0x7e;
    printf( "%d\n", lights);
    delay();
    lights = 0x00;
    printf( "%d\n", lights);
    delay();
    return;
}

int main()
{
    char    flags;
    if( flags & 0x01)
        hazard();
    if( flags & 0x02)
        left();
    if( flags & 0x04)
        right();
    return 0;
}
