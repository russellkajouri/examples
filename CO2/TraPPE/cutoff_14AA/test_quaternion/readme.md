## Unbiased molecular insertion orientations in LAMMPS GCMC

Molecular insertion in GCMC requires sampling both a position and an orientation. For an unbiased orientation proposal, no direction should be preferred, and the sampled distribution should not depend on the molecule’s initial orientation in its template.

The existing LAMMPS `fix gcmc` insertion sampler does not satisfy this requirement. This affects both the standard and `full_energy` insertion paths.

Random sampling is not necessarily unbiased sampling. The issue is how the random numbers are converted into molecular orientations.

### What does the existing sampler do?

The existing method:

1. Generates an isotropically distributed unit rotation axis, $\mathbf n$.
2. Samples a rotation angle uniformly: $\theta\sim U[0,2\pi)$.
3. Constructs a quaternion from that axis and angle.

The axis sampling is appropriate. However, combining a uniform axis with a uniform angle does **not** produce uniformly distributed three-dimensional orientations.

Small rotation angles keep the molecule close to its template orientation, regardless of the selected axis. The resulting distribution therefore retains a preference for the original template orientation.

### What should the rotation-angle distribution look like?

To compare rotations consistently, use their shortest rotation angle, called the *principal angle*, $\alpha\in[0,\pi]$.

For example, a rotation of $300^\circ$ around one axis is equivalent to a rotation of $60^\circ$ around the opposite axis. Therefore,

$$ \alpha=\min(\theta,2\pi-\theta). $$

For a normalized quaternion in LAMMPS order \((q_w,q_x,q_y,q_z)\), this angle is

$$ \alpha=2\arccos(|q_w|). $$

#### Existing sampler

The original angle $\theta$ has density $1/(2\pi)$. Each principal angle receives contributions from two original angles: $\theta=\alpha$ and $\theta=2\pi-\alpha$.

Adding these contributions gives

$$
p_{\mathrm{old}}(\alpha)
=\frac{1}{2\pi}+\frac{1}{2\pi}
=\frac{1}{\pi}.
$$

Thus, the existing sampler produces a flat principal-angle histogram.

#### Uniform orientations

Uniform orientations require a different angle distribution because equal angle intervals do not contain equal amounts of rotation space. </br>
A unit quaternion can be written as

$$
q=\left(\cos t,\mathbf n\sin t\right),
\qquad t=\alpha/2.
$$

At a fixed $t$, the three vector components lie on a spherical surface of radius $\sin t$. Its area is proportional to $\sin^2t$. Consequently, the probability density of the rotation angle must be proportional to

$$
\sin^2(\alpha/2).
$$

Normalizing this density over $[0,\pi]$ gives

$$
\begin{equation}
p_{\mathrm{uniform}}(\alpha) =
\frac{\sin^2(\alpha/2)} {\displaystyle\int_0^\pi\sin^2(a/2)\,da} = \frac{2}{\pi}\sin^2(\alpha/2) = \frac{1-\cos\alpha}{\pi}.
\end{equation}
$$

The corresponding cumulative distribution function is

$$
\begin{equation}
F_{\mathrm{uniform}}(\alpha)
=\int_0^\alpha p_{\mathrm{uniform}}(a)\,da
=\frac{\alpha-\sin\alpha}{\pi}.
\end{equation}
$$

These expressions describe uniform sampling over three-dimensional rotations, also called *Haar-uniform sampling*.

**A flat rotation-angle histogram is therefore not the correct reference for uniform orientations.**


## A simple test for the bias

Another diagnostic is to follow a direction attached to the molecule. </br>
Let $\mathbf e$ be a unit vector in the original template, and let $R\,\mathbf e$ be that vector after applying a proposed rotation. </br>
For uniform orientations, the rotated vector points equally in all directions. Its average projection onto the original direction must therefore vanish:

$$
\left\langle\mathbf e\cdot R\mathbf e\right\rangle=0.
$$

For a rotation about $\mathbf n$ through angle $\theta$, this projection is

$$
\mathbf e\cdot R\mathbf e = \cos\theta +
(1-\cos\theta)(\mathbf n\cdot\mathbf e)^2.
$$

The old sampler has

$$
\langle\cos\theta\rangle=0,
\qquad
\left\langle(\mathbf n\cdot\mathbf e)^2\right\rangle=\frac13.
$$

Because the axis and angle are sampled independently,

$$
\left\langle\mathbf e\cdot R\mathbf e\right\rangle_{\mathrm{old}}
=\frac13.
$$

This nonzero average directly demonstrates a preference for the original template direction.

For linear $\rm CO_2$, the two ends are physically equivalent. A sign-independent diagnostic is therefore also useful:

$$
P_2(c)=\frac{3c^2-1}{2},
\qquad c=\mathbf e\cdot R\mathbf e.
$$

Uniform orientations give $\langle P_2(c)\rangle=0$, whereas the old sampler gives $1/5$. This detects the bias without distinguishing the two ends of the molecule.

### Why does this matter for detailed balance?

Metropolis–Hastings does not require every proposal to be uniform. It requires the acceptance probability to account for how often each transition is proposed:

$$
A(X\rightarrow Y)=
\min\left[
1,
\frac{\pi(Y)\,T(Y\rightarrow X)}
     {\pi(X)\,T(X\rightarrow Y)}
\right].
$$

Here, $\pi$ is the desired equilibrium probability density, and (T) is the proposal probability density.

A biased orientation proposal can be valid if its bias is included in the acceptance rule. Orientations proposed more frequently require a corresponding correction.

The existing GCMC insertion and deletion acceptance expressions assume uniform orientation proposals. Using the old nonuniform sampler with those expressions therefore does not generally satisfy detailed balance for the intended equilibrium distribution.

The correction is to generate uniform orientations, consistent with the existing acceptance expressions.

This issue concerns insertion orientations. Rotational moves of existing molecules can use bounded rotation angles and remain valid when forward and inverse proposals are equally likely.

## Corrected quaternion sampler

Generate three independent uniform random numbers:

$$
u_1,u_2,u_3\sim U[0,1).
$$

Construct the quaternion in LAMMPS order:

$$
\begin{aligned}
q_w &= \sqrt{u_1}\cos(2\pi u_3),\\
q_x &= \sqrt{1-u_1}\sin(2\pi u_2),\\
q_y &= \sqrt{1-u_1}\cos(2\pi u_2),\\
q_z &= \sqrt{u_1}\sin(2\pi u_3).
\end{aligned}
$$

This samples the unit-quaternion sphere uniformly and therefore generates uniform three-dimensional orientations. The quaternion has unit norm in exact arithmetic:

$$
q_w^2+q_x^2+q_y^2+q_z^2=1.
$$

Both insertion paths use the same sampling helper.

## Numerical validation

The sampling comparison uses a pure CO₂ system at

$$
T=338\,\mathrm{K},
\qquad
\mu=-8.1\,\mathrm{kcal/mol},
$$

chosen to provide frequent exchange attempts.

Quaternions are recorded immediately after generating each insertion orientation, before energy evaluation or acceptance. Both accepted and rejected proposals are included.

The comparison checks:

- The principal-angle histogram against the predicted old and uniform densities.
- The empirical cumulative distribution against $F_{\mathrm{uniform}}(\alpha)$.
- Molecular-direction statistics against their analytical expectations.
- Quaternion norms.

The proposal distribution itself does not depend on temperature or chemical potential; these conditions provide a practical setting for collecting samples.

Accepted orientations are not expected to be uniform in general, because interactions and geometry can favor particular orientations. The tests above examine the **proposal distribution**, before those physical selection effects.

Confinement motivates correct orientation sampling because insertion feasibility and energy can depend strongly on molecular alignment. No confinement-specific results are claimed here.