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

      pythonVersion = "3.10.1";
      pkgs = import nixpkgs { inherit system; };
      myPython = nixpkgs-python.packages.${system}.${pythonVersion};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          myPython
          pkgs.nodejs_20
          pkgs.nodePackages.pnpm
          pkgs.nushell
          (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
            requests
            fastapi
            pydantic
            uvicorn
          ]))
          pkgs.util-linux # Provides libuuid
          pkgs.stdenv.cc.cc.lib # Provides libstdc++
          pkgs.alsa-lib # Often needed for Speech SDK audio
          pkgs.openssl
        ];
        shellHook = ''
          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [ 
            pkgs.util-linux 
            pkgs.stdenv.cc.cc.lib 
            pkgs.alsa-lib 
            pkgs.openssl 
          ]}"
        '';
      };
    };
}