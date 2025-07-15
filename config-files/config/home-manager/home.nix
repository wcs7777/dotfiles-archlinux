{pkgs, ...}: {
    home.username = "wcs";
    home.homeDirectory = "/home/wcs";
    home.stateVersion = "24.11"; # Comment out for error with "latest" version
    programs.home-manager.enable = true;
    home.packages = [
        pkgs.nodejs
    ];
}
