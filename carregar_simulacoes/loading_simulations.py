from scipy.io import loadmat
import re


class Simulacao():
    def __init__(self, file):
        self.file = file

    def file_pattern(self):
        pattern_no = r'N3819'
        pattern_fase_a = r'_FA_'
        pattern_fase_b = r'_FB_'

        return bool(re.search(pattern_no, self.file)), bool(re.search(pattern_fase_a, self.file)), (
            bool(re.search(pattern_fase_b, self.file)))

    def loading(self):
        data = loadmat(self.file)
        flag_N3819, flag_fase_a, flag_fase_b = self.file_pattern()
        if flag_N3819:
            if flag_fase_a:
                self.sinais_dict = {'Va': data['v6181a'].flatten(), 'Vb': data['v6181b'].flatten(), 'Vc': data['v6181c'].flatten(),
                            'Ia': data['iX0123a6181a'].flatten(), 'Ib': data['iX0123b6181b'].flatten(), 'Ic': data['iX0123c6181c'].flatten(),
                            'Ineutro': data['iTerraXx0111'].flatten(), 'Ifalta_fonte': data['iSourcXx0129'].flatten(), 'Ifalta_carga': data['iLoadXx0124'].flatten(),
                            'Vfalta_fonte': data['vSo_a'].flatten(), 'Vfalta_carga': data['vLo_a'].flatten(), 'time': data['t'].flatten()}

            elif flag_fase_b:
                self.sinais_dict = {'Va': data['v6181a'].flatten(), 'Vb': data['v6181b'].flatten(), 'Vc': data['v6181c'].flatten(),
                            'Ia': data['iX0123a6181a'].flatten(), 'Ib': data['iX0123b6181b'].flatten(), 'Ic': data['iX0123c6181c'].flatten(),
                            'Ineutro': data['iTerraXx0111'].flatten(), 'Ifalta_fonte': data['iSourcXx0129'].flatten(), 'Ifalta_carga': data['iLoadXx0124'].flatten(),
                            'Vfalta_fonte': data['vSo_b'].flatten(), 'Vfalta_carga': data['vLo_b'].flatten(), 'time': data['t'].flatten()}
            else:
                self.sinais_dict = {'Va': data['v6181a'].flatten(), 'Vb': data['v6181b'].flatten(), 'Vc': data['v6181c'].flatten(),
                            'Ia': data['iX0123a6181a'].flatten(), 'Ib': data['iX0123b6181b'].flatten(), 'Ic': data['iX0123c6181c'].flatten(),
                            'Ineutro': data['iTerraXx0111'].flatten(), 'Ifalta_fonte': data['iSourcXx0129'].flatten(), 'Ifalta_carga': data['iLoadXx0124'].flatten(),
                            'Vfalta_fonte': data['vSo_c'].flatten(), 'Vfalta_carga': data['vLo_c'].flatten(), 'time': data['t'].flatten()}
        else:
            if flag_fase_a:
                self.sinais_dict = {'Va': data['v6181a'].flatten(), 'Vb': data['v6181b'].flatten(), 'Vc': data['v6181c'].flatten().flatten(),
                            'Ia': data['iX0124a6181a'].flatten(), 'Ib': data['iX0124b6181b'].flatten(), 'Ic': data['iX0124c6181c'].flatten(),
                            'Ineutro': data['iTerraXx0111'].flatten(), 'Ifalta_fonte': data['iSourcXx0130'].flatten(), 'Ifalta_carga': data['iLoadXx0125'].flatten(),
                            'Vfalta_fonte': data['vSo_a'].flatten(), 'Vfalta_carga': data['vLo_a'].flatten(), 'time': data['t'].flatten()}
            elif flag_fase_b:
                self.sinais_dict = {'Va': data['v6181a'].flatten(), 'Vb': data['v6181b'].flatten(), 'Vc': data['v6181c'].flatten(),
                            'Ia': data['iX0124a6181a'].flatten(), 'Ib': data['iX0124b6181b'].flatten(), 'Ic': data['iX0124c6181c'].flatten(),
                            'Ineutro': data['iTerraXx0111'].flatten(), 'Ifalta_fonte': data['iSourcXx0130'].flatten(), 'Ifalta_carga': data['iLoadXx0125'].flatten(),
                            'Vfalta_fonte': data['vSo_b'].flatten(), 'Vfalta_carga': data['vLo_b'].flatten(), 'time': data['t'].flatten()}
            else:
                self.sinais_dict = {'Va': data['v6181a'].flatten(), 'Vb': data['v6181b'].flatten(), 'Vc': data['v6181c'].flatten(),
                            'Ia': data['iX0124a6181a'].flatten(), 'Ib': data['iX0124b6181b'].flatten(), 'Ic': data['iX0124c6181c'].flatten(),
                            'Ineutro': data['iTerraXx0111'].flatten(), 'Ifalta_fonte': data['iSourcXx0130'].flatten(), 'Ifalta_carga': data['iLoadXx0125'].flatten(),
                            'Vfalta_fonte': data['vSo_c'].flatten(), 'Vfalta_carga': data['vLo_c'].flatten(), 'time': data['t'].flatten()}

        return self.sinais_dict
