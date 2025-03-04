{
  description = "Agentic Trading System";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = pkgs.mkShell {
            name = "trading-system";
            
            buildInputs = with pkgs; [
              # Python and packages
              (python312.withPackages (ps: with ps; [
                # Core dependencies
                pandas
                numpy
                fastapi
                uvicorn
                python-dotenv
                sqlalchemy
                pydantic
                # Data and visualization
                plotly
                dash
                # Testing
                pytest
                pytest-asyncio
                pytest-cov
                httpx
                # Database
                psycopg2
                redis
                # Task queue
                celery
              ]))
              poetry
              
              # Node.js and related tools
              nodejs_20
              typescript
              yarn
              
              # Other tools
              docker
              docker-compose
              direnv
              uv
            ];
            
            shellHook = ''
              export PYTHONPATH=$PYTHONPATH:${toString ./.}
              echo "Welcome to the Trading System development environment!"
            '';
          };
        }
      );
    };
}
