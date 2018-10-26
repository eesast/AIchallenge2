#include"playerAI.h"

void (*jump)(Position a) = nullptr;
void bind_api(void(*func)(Position))
{
    jump = func;
}
void play_game()
{
    using namespace std;
    cout << "player" << endl;
    (*jump)(Position{ 1,2 });
    return;
}
