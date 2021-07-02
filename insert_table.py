
class CalibrationData():
    def __init__(self, first_lvl, last_lvl, volume, medium_volume):
        self.main_lvl = self.main_level_list(first_lvl, last_lvl)
        # print('main', self.main_lvl)
        self.main_vlv_vol = self.unite_level_volume(self.main_lvl,
                                                    volume)
        # print('main lvl vol', self.main_vlv_vol)
        self.tmp_dict = self.make_tmp_dict(self.main_lvl,
                                           self.main_vlv_vol)
        # print('tmp', self.tmp_dict)
        self.medium_lvl_vol = self.medium_level_volume(first_lvl,
                                                       last_lvl,
                                                       medium_volume,
                                                       self.tmp_dict)

    def main_level_list(self, first_lvl, last_lvl):
        list = []
        for i in range(first_lvl, last_lvl + 1):
            if (i % 10) == 0:
                list.append(i)
        return list

    def unite_level_volume(self, level, volume):
        res = list(zip(level, volume))
        return res

    def make_tmp_dict(self, level, lvl_vol):
        res = {}
        for key, value in zip(level, lvl_vol):
            res[str(key)] = value
        return res

    def medium_level_volume(self, first_lvl, last_lvl,
                            medium_volume, tmp_dict):
        list =  []
        for i in range (first_lvl, last_lvl + 1):
            tmp = []
            if (i % 10) == 0:
                continue
            tmp.append(i)
            data = tmp_dict[str(i - (i % 10))][1] + medium_volume[str(i % 10)]
            tmp.append(round(data, 3))
            list.append(tuple(tmp))
        return list

class RgsTank():
    def make_rgs_list(self, first_level, last_level,
                      volume_list, step_list, for_rvs):
        super_list = []
        if for_rvs:
            last_level = last_level + 10
        else:
            last_level = last_level + 1
        for level in range(first_level, last_level):
            # print(level)
            tmp_list = []
            pos = level // 10
            i = level % 10
            volume = volume_list[pos] + (step_list[pos] * i)
            tmp_list.append(level)
            tmp_list.append(round(volume, 3))
            super_list.append(tuple(tmp_list))
        return super_list
