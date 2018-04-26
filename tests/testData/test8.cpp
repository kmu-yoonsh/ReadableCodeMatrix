#include<iostream>

using namespace std;

int main()
{
    int temp = 1;
    int num = 2;

    if(temp % 2)
    {
        if(!(temp % 4))
            temp = temp + 1;
        else if(5 % temp)
            cout << '!' << endl;
    }


    return 0;
}