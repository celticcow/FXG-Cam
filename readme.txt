SSPC Cam Tunnel Lockdown

input site code <4-letter>
input site code <3-number>

need group SSPC-SICK-<letter>-<num>
need group SSCP-Autodim-<letter>-<num>

input list of Cam Tunnel Controllers
input list of SSCP-SICK
input list of SSCP-Autodim

verify input list of SSCP matches existing groups
verify existing sscp site groups exist inside of SSCP-Autodim and SSCP-Sick respectivly 

create group CamTunController-<num>
put new site CamTunController into group Camera-Tunnel-Controller  group

create rules at bottom of section  CamTunnel-Lockdown 

sscp-<letter>1    any -> (CamTunController-<num>, sspc-sick-<letter>-<num>, sscp-autodim-<letter>-<num>)
sscp-<letter>2    (CamTunController-<num>, sspc-sick-<letter>-<num>, sscp-autodim-<letter>-<num>) -> any
