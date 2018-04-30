#include<iostream>

using namespace std;

int num = 10;
int number = 1;

void e()
{
    num = 11;
}

void d()
{
    e();
}

void c()
{
    d();
}

void b()
{
    c();
}

void a()
{
    b();
}


int main()
{
    int temp = 1;
    num = 9;
    number 10;
    if(temp % 2)
    {
        if(!(temp % 4))
            temp = temp + 1;
        else if(5 % temp)
            a();
    }

    return 0;
}