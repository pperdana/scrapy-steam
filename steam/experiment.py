platform_ls = ['platform_img win', 'platform_img mac',
               'platform_img linux', 'vr_supported']


def get_platform(ls_platform):
    platform = [item.split(' ')[-1] for item in platform_ls]
    return platform


print(get_platform(platform_ls))
