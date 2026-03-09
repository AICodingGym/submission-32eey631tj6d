from distutils.version import LooseVersion

def minversion_test(have_version, version, inclusive=True):
    have_parts = LooseVersion(have_version).version
    req_parts = LooseVersion(version).version
    max_len = max(len(have_parts), len(req_parts))
    
    for i in range(max_len):
        hp = have_parts[i] if i < len(have_parts) else -1
        rp = req_parts[i] if i < len(req_parts) else -1
        
        hp_val = (1, hp) if isinstance(hp, int) else (0, hp)
        rp_val = (1, rp) if isinstance(rp, int) else (0, rp)
        
        if hp_val == rp_val:
            continue
            
        if inclusive:
            return hp_val >= rp_val
        else:
            return hp_val > rp_val
            
    return inclusive

test_cases = [
    # have, req, inclusive, expected
    ('1.14.3', '1.14dev', True, True),
    ('1.14', '1.14dev', True, True),
    ('1.14dev', '1.14', True, False),
    ('1.14.3', '1.14.3', True, True),
    ('1.14.3', '1.14.3', False, False),
    ('1.14.4', '1.14.3', True, True),
    ('1.14.4', '1.14.3', False, True),
    ('1.14dev', '1.14.3', True, False),
    ('1.14', '1.14.0', True, False), # 1.14 < 1.14.0 since missing is -1
    ('1.14.0', '1.14', True, True),
    ('1.14rc1', '1.14dev', True, True),
]

for have, req, inc, exp in test_cases:
    res = minversion_test(have, req, inc)
    print(f"{have} {'>=' if inc else '>'} {req} = {res} (Expected {exp}) {'PASS' if res == exp else 'FAIL'}")

