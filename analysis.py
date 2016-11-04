import numpy as np
from dtensor import dtensor
from ktensor import ktensor
from cp import als
import numpy as np


magnetic = [(51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.74879455566406), (51.24528503417969, -6.518707275390625, -64.7525544387102), (51.24528503417969, -6.518707275390625, -64.77583043932914), (51.24528503417969, -6.518707275390625, -64.79910643994808), (51.24528503417969, -6.518707275390625, -64.82238244056701), (51.24528503417969, -6.518707275390625, -64.84565844118595), (51.24528503417969, -6.518707275390625, -64.86893444180488), (51.24528503417969, -6.518707275390625, -64.89221044242382), (51.24528503417969, -6.518707275390625, -64.91548644304275), (51.24528503417969, -6.527138935583643, -64.93876244366169), (51.24528503417969, -6.538270278358832, -64.96203844428062), (51.24528503417969, -6.54940162113402, -64.98531444489956), (51.24528503417969, -6.560532963909209, -65.0085904455185), (51.24528503417969, -6.571664306684397, -65.03186644613743), (51.24528503417969, -6.582795649459586, -65.04762268066406), (51.24528503417969, -6.593926992234774, -65.04762268066406), (51.24528503417969, -6.6050583350099625, -65.04762268066406), (51.24528503417969, -6.616189677785151, -65.04762268066406), (51.2427298237104, -6.6273210205603394, -65.04762268066406), (51.24009185461793, -6.638452363335528, -65.04762268066406), (51.23745388552547, -6.6495837061107155, -65.04762268066406), (51.234815916433, -6.660715048885904, -65.04762268066406), (51.23217794734053, -6.671846391661092, -65.04762268066406), (51.22953997824807, -6.682977734436281, -65.04762268066406), (51.2269020091556, -6.694109077211469, -65.04762268066406), (51.22426404006313, -6.705240419986658, -65.04762268066406), (51.22162607097067, -6.716371762761846, -65.04762268066406), (51.2189881018782, -6.727503105537035, -65.04187399918679), (51.216350132785735, -6.738634448312223, -65.03001136835664), (51.21371216369327, -6.7440338134765625, -65.0181487375265), (51.211074194600805, -6.7440338134765625, -65.00628610669635), (51.208436225508336, -6.7440338134765625, -64.9944234758662), (51.205798256415875, -6.7440338134765625, -64.98256084503606), (51.203160287323406, -6.7440338134765625, -64.97069821420591), (51.200522318230945, -6.7440338134765625, -64.95883558337577), (51.19788434913848, -6.7440338134765625, -64.94697295254562), (51.19524638004601, -6.7440338134765625, -64.93511032171547), (51.19260841095355, -6.7440338134765625, -64.92324769088533)]
gyro = [(-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569), (-0.1796834787476462, -0.2340431239700166, -0.10636372446056569)]
accel = [(0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375), (0.2248077392578125, -0.5124053955078125, -0.81341552734375)]



x = np.array([ n[0] + n[1] + n[2] for n in zip(gyro, accel, magnetic) ])
T_in= dtensor(x.reshape(50,3,3))
T_out, fit, itr, _ = als(T_in, 3)
np.allclose(T_in, T_out.totensor())