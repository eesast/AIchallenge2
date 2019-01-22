#ifndef SOUND_H
#define SOUND_H

#include "constant.h"

class Sound
{
  public:
    enum class SOUND_TYPE
    {
        FOOTSTEP_SOUND = 0,
        GUN_SOUND = 1,
        RADIO_VOICE = 2
    };

    Sound();
    Sound(Sound &&) = default;
    Sound(const Sound &) = default;
    Sound &operator=(Sound &&) = default;
    Sound &operator=(const Sound &) = default;
    ~Sound();

  private:
    SOUND_TYPE _sound_type;
    int _emitter;
    int _receiver;
    int _data;
};

#endif // !SOUND_H