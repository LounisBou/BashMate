class CaddyMercure < Formula
    desc "Custom build of Caddy server using xcaddy with Mercure module"
    homepage "https://caddyserver.com/"
    url "https://github.com/caddyserver/caddy/archive/refs/tags/v2.8.4.tar.gz"
    sha256 "5c2e95ad9e688a18dd9d9099c8c132331e01e0bebd401183e8d9123372cf4fcc"
    license "Apache-2.0"
  
    depends_on "go" => :build
  
    def install
      # Path to the output binary
      output_path = buildpath/"caddy-mercure"
  
      # Build Caddy with Mercure using the globally installed xcaddy
      system "xcaddy", "build", "--with", "github.com/dunglas/mercure/caddy", "--output", output_path
  
      # Install the built binary as "caddy-mercure" to avoid conflicts with existing Caddy installations
      bin.install output_path => "caddy-mercure"
    end
  
    # Define the service for Homebrew
    service do
      run [opt_bin/"caddy-mercure", "run", "--config", "/opt/homebrew/etc/Caddyfile"]
      keep_alive true
      working_dir var
      log_path var/"log/caddy-mercure.log"
      error_log_path var/"log/caddy-mercure-error.log"
    end
  
    test do
      # Check if the binary runs correctly
      output = shell_output("#{bin}/caddy-mercure version")
      assert_match "v2.8.4", output
    end
  end  