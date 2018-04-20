#include <iostream>

int main()
{
    int temp = 1;
    int num = 2;

    if(temp)
        temp += int(temp/2);
    else
        temp += 10;

    if(num)
        num += temp;
    else
        temp = num;

    return 0;
}