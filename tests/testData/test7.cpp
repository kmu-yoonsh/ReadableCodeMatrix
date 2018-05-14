#include<iostream>

using namespace std;

int main()
{
    int temp = 1;
    int num = 2;

    if((temp % 2) && 1 > num)
    {
        if(!(temp % 4))
            std::cout << temp << endl;
        else if(5 % temp)
            std::cout << '!' << endl;
    }


    return 0;
}