import random

class person:
    def __init__(self,hp,xp,name,damage,id,status):
        self.name=name
        self.hp=hp
        self.max_hp=hp
        self.xp=xp
        self.damage=damage
        self.id=id
        self.status=status

    def get_name(self):
        return self.name

    def get_damage(self):
        return self.damage
    
    def get_hp(self):
        return self.hp

    def get_xp(self):
        return self.xp
    
    def get_maxhp(self):
        return self.max_hp

    def generate_damage(self):
        dmg=random.randrange(self.damage-5,self.damage+5)
        return dmg

    def take_damage(self,damage):
        self.hp=self.hp-damage
        print(self.hp)
        if self.hp>self.max_hp:
            self.hp=self.max_hp
            return self.max_hp
        elif self.hp<=0:
            self.hp=0
            return self.hp
    
    def reduce_xp(self,change):
        self.xp-=change

    def get_id(self):
        return self.id

    def get_status(self):
        return self.status

class _member:
    def __init__(self,name,mem_id,xp,hp,dmg,hp_level,dmg_level):
        self.name=name
        self.id=mem_id
        self.mem_xp=xp
        self.mem_max_hp=hp
        self.mem_dmg=dmg
        self.hp_level=hp_level
        self.dmg_level=dmg_level
    def get_member_name(self):
        return self.name
    def get_id(self):
        return self.id
    def get_member_xp(self):
        return self.mem_xp
    def get_member_damage(self):
        return self.mem_dmg
    def get_member_max_hp(self):
        return self.mem_max_hp
    def get_member_damage_level(self):
        return self.dmg_level
    def get_member_hp_level(self):
        return self.hp_level
    


