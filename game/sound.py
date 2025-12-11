"""
사운드 시스템 (간단 버전 - 효과음 없이도 작동)
"""

import pygame
import os


class SoundSystem:
    """게임 사운드 관리"""
    
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        self.music_volume = 0.3
        self.sfx_volume = 0.5
        
        try:
            pygame.mixer.init()
        except:
            self.enabled = False
            print("Warning: Sound system not available")
    
    def load_sounds(self):
        """효과음 로드 (파일이 있다면)"""
        if not self.enabled:
            return
        
        sound_files = {
            'dash': 'dash.wav',
            'hit': 'hit.wav',
            'key': 'key_collect.wav',
            'wall': 'wall_place.wav',
            'noise': 'noise.wav',
            'clear': 'stage_clear.wav',
            'game_over': 'game_over.wav'
        }
        
        for name, filename in sound_files.items():
            path = os.path.join('assets', 'sounds', filename)
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(self.sfx_volume)
                except:
                    pass
    
    def play_sound(self, name):
        """효과음 재생"""
        if self.enabled and name in self.sounds:
            try:
                self.sounds[name].play()
            except:
                pass
    
    def play_music(self, filename, loops=-1):
        """배경음악 재생"""
        if not self.enabled:
            return
        
        path = os.path.join('assets', 'music', filename)
        if os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops)
            except:
                pass
    
    def stop_music(self):
        """배경음악 정지"""
        if self.enabled:
            try:
                pygame.mixer.music.stop()
            except:
                pass
    
    def set_music_volume(self, volume):
        """배경음악 볼륨 설정 (0.0 ~ 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.enabled:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except:
                pass
    
    def set_sfx_volume(self, volume):
        """효과음 볼륨 설정 (0.0 ~ 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
