"""SONIC G1 reference encoder contract and term-major ten-frame proprioception."""
import numpy as np
from scipy.spatial.transform import Rotation as R
from motion_challenge.adapters.onnx import ONNXController


def heading(rotation):
    q=rotation.as_quat();zw=q[2:]
    norm=np.linalg.norm(zw)
    return R.identity() if norm<1e-12 else R.from_quat([0.,0.,*(zw/norm)])


class SONIC(ONNXController):
    def frame(self,state):
        q,qd,w,g,r=self.proprio(state)
        return [w,q-self.default,qd,self.last,g]

    def reset(self,state,reference,seed):
        super().reset(state,reference,seed)
        self.history=[np.tile(v,(10,1)).astype(np.float32) for v in self.frame(state)]
        self.align=heading(R.from_quat(state.root_orientation_xyzw))*heading(R.from_quat(reference[0].root_orientation_xyzw)).inv()

    def observations(self,state,reference):
        self.history=[np.concatenate([h[1:],np.asarray(v,np.float32)[None]]) for h,v in zip(self.history,self.frame(state))]
        q=np.array([f.joint_position_rad for f in reference])[:,self.order]
        qd=np.array([f.joint_velocity_rad_s for f in reference])[:,self.order]
        rotations=R.from_quat([f.root_orientation_xyzw for f in reference])
        rel=(R.from_quat(state.root_orientation_xyzw).inv()*self.align*rotations).as_matrix()[:,:,:2]
        return {'g1_input':np.r_[q.reshape(-1),qd.reshape(-1),rel.reshape(-1)],
                'proprioception':np.concatenate([h.reshape(-1) for h in self.history])}


def create(root,runtime):return SONIC(root,runtime)
