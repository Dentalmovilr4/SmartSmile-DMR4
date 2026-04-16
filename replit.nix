{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.libGL
    pkgs.libGLU
    pkgs.glib
  ];
}