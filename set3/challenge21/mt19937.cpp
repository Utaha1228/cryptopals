#include<bits/stdc++.h>
using namespace std;

mt19937 rng(0);

int main(){
	for(int i = 0; i < 900; i++){
		rng();
	}
	for(int i = 0; i < 10; i++){
		cout<<rng()<<'\n';
	}
}