#include <stdio.h>
#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

int tri[101];
int T,K,temp;

int main()
{
    for(int i=0; i<101; i++)
    {
        tri[i+1] = tri[i] + (i+1);
        //cout << tri[i];
    }
    cin >> T;
here:
    while(T--)
    {
        cin >> K;
        for(int i=1; i<101;i++)
        {
            for(int j=1; j<101; j++)
            {
                for(int k=1; k<101; k++)
                {
                    temp = tri[i] + tri[j] + tri[k];
                    if(temp == K)
                    {

                        cout << 1 << endl;
                        goto here;
                    }
                }
            }
        }
        cout << 0 << endl;
    }
    return 0;
}