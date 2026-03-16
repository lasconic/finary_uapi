import finary_uapi.user_fonds_euro as fe
import finary_uapi.user_startups as st
import finary_uapi.user_precious_metals as pm
import finary_uapi.user_crowdlendings as cl

print("fonds_euro:", [f for f in dir(fe) if f.startswith('get')])
print("startups:", [f for f in dir(st) if f.startswith('get')])
print("precious_metals:", [f for f in dir(pm) if f.startswith('get')])
print("crowdlendings:", [f for f in dir(cl) if f.startswith('get')])