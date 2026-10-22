read "../ModelCore.mpl":
xvars := [x(t), v(t)]:
uvars := [F(t)]:
pvars := [m, k, c]:
ode_eqns := [diff(x(t),t)=v(t), m*diff(v(t),t)+c*v(t)+k*x(t)=F(t)]:
usr_funcs := []:
M := ModelCore:-Model(name="MassSpringDamper", time=t,
    xvars=xvars, uvars=uvars, pvars=pvars,
    usr_funcs=usr_funcs, ode_eqns=ode_eqns):
ModelCore:-Summary(M):
print(ModelCore:-Validate(M)):
# ModelCore:-ExportIR(M, "model.ir.json"):
