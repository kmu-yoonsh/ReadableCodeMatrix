#include<iostream>

using namespace std;

int main()
{
    int temp = 1;

    if(temp)
        if(temp % 2)
            std::cout << temp << std::endl;

    if(temp)
    {
        if(!(temp % 3))
        {
            cout << temp << endl;
        }
    }

    if(temp)
    {
        if(!(temp % 4))
            std::cout << temp << endl;
        else
            std::cout << 3 << endl;
    }

    if(temp)
    {
        if(!(temp % 4))
            std::cout << temp << endl;
        else if(!(temp % 3))
            std::cout << 3 << endl;
    }


    return 0;
}