#include <iostream>  // std::cout
#include <algorithm> // std::stable_sort
#include <vector>    // std::vector
#include <array>
using namespace std;

bool compare_as_ints(double i, double j)
{
    return (int(i) < int(j));
}

bool IsOdd(int i)
{
    return ((i % 2) == 1);
}

bool IsEven(int i)
{
    return ((i % 2) == 0);
}

bool myfunction(int i, int j)
{
    return (i == j);
}

void myfunction_for_each(int i)
{ // function:
    std::cout << ' ' << i;
}

int main()
{
    std::array<int, 8> foo = {3, 5, 7, 11, 13, 17, 19, 24};

    if (std::all_of(foo.begin(), foo.end(), IsOdd))
        std::cout << "All the elements are odd numbers.\n";
    else
    {
        std::cout << "All elements are not odd";
    }


    cout << "\n";

    if (std::any_of(foo.begin(), foo.end(), IsEven))
        std::cout << "There are Even elements in the range.\n";

    cout << "\n";


    //int moo[] = {10,20,100};
    //vector<int> myvector(moo,moo+3);
    vector<int> myvector;
    myvector.push_back(10);
    myvector.push_back(20);
    myvector.push_back(30);


    cout << "myvector contains:";
    for_each(myvector.begin(), myvector.end(), myfunction_for_each);
    cout << '\n';




    int myints[] = {10, 20, 30, 40};
    int *p;

    p = std::find(myints, myints + 4, 30);
    if (p != myints + 4)
        std::cout << "Element found in myints: " << *p << '\n';
    else
        std::cout << "Element not found in myints\n";

    // using std::find with vector and iterator:
    std::vector<int> myvectors(myints, myints + 4);
    std::vector<int>::iterator it;

    it = find(myvectors.begin(), myvectors.end(), 30);
    if (it != myvectors.end())
        std::cout << "Element found in myvector: " << *it << '\n';
    else
        std::cout << "Element not found in myvector\n";




    



    cout << "\n";
    return 0;
}