# ModelCore.Maple prototype v0.2
# This package is a draft and has not been executed in Maple.
# The model is represented using Maple time-dependent functions (case A).
ModelCore := module()
option package;
export Model, NormalizeResiduals, Validate, Summary, ExportIR;

Model := proc({name::string := "unnamed", version::string := "0.1.0",
               time::name := t, xvars::list := [], uvars::list := [],
               pvars::list := [], usr_funcs::list := [], ode_eqns::list := []})
    local M;
    M := table();
    M["name"] := name; M["version"] := version;
    M["time"] := time; M["xvars"] := xvars;
    M["uvars"] := uvars; M["pvars"] := pvars;
    M["usr_funcs"] := usr_funcs; M["ode_eqns"] := ode_eqns;
    M["residuals"] := NormalizeResiduals(ode_eqns);
    return M;
end proc;

NormalizeResiduals := proc(eqns::list)
    local e;
    return [seq(`if`(type(e, equation), lhs(e)-rhs(e), e), e in eqns)];
end proc;

Validate := proc(M::table)
    local vars, t0, e, s, dx, issues;
    issues := [];
    t0 := M["time"];
    vars := [op(M["xvars"]), op(M["uvars"]), op(M["pvars"])];
    if nops(M["xvars"]) = 0 then
        issues := [op(issues), "No state variables declared"];
    end if;
    if nops(M["ode_eqns"]) <> nops(M["xvars"]) then
        issues := [op(issues), "Equation count differs from state count"];
    end if;
    if nops({op(vars)}) <> nops(vars) then
        issues := [op(issues), "Duplicate variables or parameters"];
    end if;
    for s in M["xvars"] do
        if not type(s, function) or not has(s, t0) then
            issues := [op(issues), cat("Invalid time-dependent state: ", convert(s,string))];
        end if;
    end do;
    return issues;
end proc;

Summary := proc(M::table)
    printf("Model: %s (%s)\n", M["name"], M["version"]);
    printf("States: %d, inputs: %d, parameters: %d, equations: %d\n",
           nops(M["xvars"]), nops(M["uvars"]), nops(M["pvars"]), nops(M["ode_eqns"]));
    return NULL;
end proc;

# Exports a compact descriptor; equation expressions stay in Maple source.
# JSON:-ToJSON compatibility must be checked against the target Maple version.
ExportIR := proc(M::table, filename::string)
    local payload, fd, txt;
    payload := table([
        "ir_version" = "0.2",
        "model" = table(["name"=M["name"], "version"=M["version"]]),
        "time" = convert(M["time"],string),
        "states" = map(s->convert(s,string), M["xvars"]),
        "inputs" = map(s->convert(s,string), M["uvars"]),
        "parameters" = map(s->convert(s,string), M["pvars"]),
        "equation_count" = nops(M["ode_eqns"])
    ]);
    txt := JSON:-ToJSON(payload);
    fd := fopen(filename, WRITE, TEXT);
    fprintf(fd, "%s\n", txt);
    fclose(fd);
    return filename;
end proc;
end module:
