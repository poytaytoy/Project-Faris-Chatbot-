{
  description = "Faris development flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    nixpkgs-python.url = "github:cachix/nixpkgs-python";
  };

  outputs = { self, nixpkgs, nixpkgs-python }: 
    let
      system = "x86_64-linux";
      # system = "x86_64-rwin";

      pythonVersion = "3.10.1"
      pkgs = import nixpkgs { inherit system; };
      myPython = nixpkgs-python.packages.${system}.${pythonVersion};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          myPython
          nodejs_24
          nodePackages.pnpm
          (yarn.override { nodejs = nodejs_24; })
        ];
        shellHook = ''
          python --version
        '';
      };
    };
}