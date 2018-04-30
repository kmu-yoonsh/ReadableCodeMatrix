#include<iostream>

using namespace std;

int num_x = 10;
int num_y = 11;
int num_z = 12;

void b()
{
    num_z = num_y;
}

void a()
{
    b();
}


int main()
{
    int temp = 1;
    num_x = 9;
    num_z = 1;
    if(temp % 2)
    {
        if(!(temp % 4))
            temp = temp + 1;
        else if(5 % temp)
            a();
    }


    return 0;
}