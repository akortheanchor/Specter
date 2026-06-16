import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import imageio
from PIL import Image
from scipy.integrate import odeint
import io, os

OUT = "/home/claude/SPECTER/assets/gifs"
os.makedirs(OUT, exist_ok=True)

C = {
    "blue":"#1565C0","red":"#C62828","green":"#2E7D32","orange":"#E65100",
    "purple":"#6A1B9A","teal":"#00695C","bg":"#0D1117","fg":"#F0F6FF",
}
plt.rcParams.update({
    "figure.facecolor":C["bg"],"axes.facecolor":C["bg"],"axes.edgecolor":"#30363D",
    "axes.labelcolor":C["fg"],"xtick.color":C["fg"],"ytick.color":C["fg"],
    "text.color":C["fg"],"grid.color":"#21262D","grid.alpha":0.5,"font.family":"monospace",
})

FIXED_W = {"banner":(1000,320),"triple":(1100,380),"double":(900,400),"square":(580,540),"net":(960,440)}

def frame(fig, sz, dpi=95):
    buf = io.BytesIO()
    fig.savefig(buf,format="png",dpi=dpi,bbox_inches="tight",facecolor=fig.get_facecolor())
    buf.seek(0); img = Image.open(buf).convert("RGB").resize(sz,Image.LANCZOS)
    plt.close(fig); return np.array(img)

def gif(frames, path, fps=13):
    imageio.mimsave(path, frames, fps=fps, loop=0)
    print(f"  ✓ {os.path.basename(path)} ({len(frames)} fr, {os.path.getsize(path)//1024} KB)")

def sir(y,t,b,g):
    S,I,R=y; N=S+I+R; return[-b*S*I/N, b*S*I/N-g*I, g*I]

rng = np.random.RandomState(42)

# ── GIF 1: Banner ─────────────────────────────────────────────────────────
print("1/6 Banner...")
frames=[]; sz=FIXED_W["banner"]
for f in range(36):
    t=f/36
    fig=plt.figure(figsize=(10,3.2),facecolor=C["bg"])
    ax=fig.add_axes([0,0,1,1]); ax.set_facecolor(C["bg"])
    ax.set_xlim(0,10); ax.set_ylim(0,3.2); ax.axis("off")
    for wire in range(5):
        y=0.3+wire*0.52; ax.axhline(y,color="#1E3A5F",lw=0.8,alpha=0.4)
        for g in range(8):
            x=((g*1.3-t*4)%10.5)-0.5
            col=[C["blue"],C["purple"],C["teal"]][g%3]
            ax.add_patch(mpatches.FancyBboxPatch((x-0.18,y-0.14),0.36,0.28,
                boxstyle="round,pad=0.02",fc=col,ec="white",lw=0.5,alpha=0.7))
            ax.text(x,y,["H","X","Z","Rx","Ry","T","S","CNOT"][g%8],
                    ha="center",va="center",fontsize=5.5,color="white",fontweight="bold")
    glow=0.6+0.3*np.sin(t*2*np.pi)
    for dx,dy in[(-0.01,0),(0.01,0)]:
        ax.text(5+dx,2.0+dy,"S P E C T E R",ha="center",va="center",fontsize=42,
                fontweight="bold",color=C["blue"],alpha=glow*0.3)
    ax.text(5,2.0,"S P E C T E R",ha="center",va="center",fontsize=42,
            fontweight="bold",color=C["fg"])
    sub="Stealth Perturbation Engine via Circuit-based Tunneling & Epidemiological Resilience"
    nc=int(len(sub)*min(1.0,t*3))
    ax.text(5,1.22,sub[:nc]+("▌" if nc<len(sub) else ""),ha="center",va="center",
            fontsize=7.5,color=C["teal"],alpha=0.9)
    for bx,bt,bc in zip([2.5,5.0,7.5],["QAPE","SIR-PACS","QPUF"],[C["red"],C["orange"],C["green"]]):
        a=min(1.0,max(0.0,(t-0.5)*3))
        ax.add_patch(mpatches.FancyBboxPatch((bx-0.62,0.22),1.24,0.58,
            boxstyle="round,pad=0.05",fc=bc,alpha=a*0.85,ec="white",lw=0.8))
        ax.text(bx,0.51,bt,ha="center",va="center",fontsize=9,color="white",fontweight="bold",alpha=a)
    frames.append(frame(fig,sz))
gif(frames,f"{OUT}/specter_banner.gif",fps=14)

# ── GIF 2: QAPE Attack ────────────────────────────────────────────────────
print("2/6 QAPE Attack...")
frames=[]; sz=FIXED_W["triple"]
clean=np.zeros((32,32))
for i in range(32):
    for j in range(32):
        r=np.sqrt((i-16)**2+(j-16)**2)
        clean[i,j]=np.exp(-r**2/80)*0.8+rng.rand()*0.04
for f in range(44):
    t=f/44
    fig,axes=plt.subplots(1,3,figsize=(11,3.8),facecolor=C["bg"])
    fig.patch.set_facecolor(C["bg"])
    axes[0].imshow(clean,cmap="gray",vmin=0,vmax=1); axes[0].axis("off")
    axes[0].set_title("Clean DICOM",color=C["fg"],fontsize=9,pad=4)
    axes[0].text(16,35,"AI: ✓ Correct",ha="center",color=C["green"],fontsize=7.5,transform=axes[0].transData)

    ax1=axes[1]; ax1.set_facecolor(C["bg"]); ax1.set_xlim(0,10); ax1.set_ylim(0,5); ax1.axis("off")
    ax1.set_title("QAOA Circuit Optimising",color=C["fg"],fontsize=9,pad=4)
    p_lay=min(7,int(t*11))
    for w in range(4):
        y=1+w*0.85
        ax1.plot([0.5,9.5],[y,y],color="#1E4A8F",lw=1.2,alpha=0.5)
        ax1.text(0.2,y,f"q{w}",color=C["teal"],fontsize=8,va="center")
        for l in range(p_lay):
            x=1.2+l*1.2
            col=[C["blue"],C["purple"],C["orange"],C["red"]][w]
            ax1.add_patch(mpatches.FancyBboxPatch((x-0.2,y-0.18),0.4,0.36,
                boxstyle="round,pad=0.03",fc=col,alpha=0.85,ec="white",lw=0.6))
            ax1.text(x,y,["Rz","Rx","Ry","H"][w],ha="center",va="center",
                     fontsize=7,color="white",fontweight="bold")
    obj=min(t*1.3,1.0)
    ax1.text(5,4.5,f"Objective: {-0.12+obj*0.95:.3f}   Layers: {p_lay}/7",
             ha="center",color=C["teal"],fontsize=7.5)

    adv_s=min(1.0,t*1.5)
    pert=np.zeros((32,32))
    for pi in range(4):
        for pj in range(4):
            s=1 if (pi+pj)%2==0 else -1
            pert[pi*8:(pi+1)*8,pj*8:(pj+1)*8]=s*0.02*adv_s
    adv=np.clip(clean+pert+rng.randn(32,32)*0.015*adv_s,0,1)
    axes[2].imshow(adv,cmap="gray",vmin=0,vmax=1); axes[2].axis("off")
    axes[2].set_title("Adversarial DICOM",color=C["fg"],fontsize=9,pad=4)
    msg = f"AI: ✗ Fooled! ({adv_s*100:.0f}%)" if adv_s>0.6 else "Perturbing..."
    col_m = C["red"] if adv_s>0.6 else C["orange"]
    axes[2].text(16,35,msg,ha="center",color=col_m,fontsize=7.5,transform=axes[2].transData)
    plt.suptitle("QAPE — Quantum Adversarial Perturbation Engine",
                 color=C["fg"],fontsize=10,fontweight="bold",y=1.01)
    plt.tight_layout(pad=0.4)
    frames.append(frame(fig,sz))
gif(frames,f"{OUT}/qape_attack.gif",fps=13)

# ── GIF 3: SIR Propagation ────────────────────────────────────────────────
print("3/6 SIR Propagation...")
frames=[]; sz=FIXED_W["triple"]
t_full=np.linspace(0,120,600); N=1000
scen=[("No Defence\n(R₀=7.0)",0.35,0.05,C["red"]),
      ("Partial\n(R₀=2.5)",0.20,0.08,C["orange"]),
      ("QPUF\n(R₀=0.53)",0.08,0.15,C["green"])]
sols=[(s,odeint(sir,[N-5,5,0],t_full,args=(b,g))) for s,b,g,_ in scen]

for f in range(48):
    ti=int((f/48)*len(t_full)); day=(f/48)*120
    fig,axes=plt.subplots(1,3,figsize=(11,3.8),facecolor=C["bg"])
    fig.patch.set_facecolor(C["bg"])
    for ax,(lbl,b,g,col),(slbl,sol) in zip(axes,scen,sols):
        S=sol[:,0]/N*100; I=sol[:,1]/N*100; R=sol[:,2]/N*100
        ax.plot(t_full,S,"-",color=C["blue"],lw=1,alpha=0.2)
        ax.plot(t_full,I,"--",color=col,lw=1,alpha=0.2)
        ax.plot(t_full,R,":",color=C["green"],lw=1,alpha=0.2)
        ax.plot(t_full[:ti],S[:ti],"-",color=C["blue"],lw=2,label="S")
        ax.plot(t_full[:ti],I[:ti],"--",color=col,lw=2.5,label="I")
        ax.plot(t_full[:ti],R[:ti],":",color=C["green"],lw=2,label="R")
        ax.fill_between(t_full[:ti],0,I[:ti],alpha=0.14,color=col)
        if ti>0: ax.plot(t_full[ti-1],I[ti-1],"o",color=col,ms=7)
        pk=np.argmax(I)
        if ti>pk:
            ax.text(t_full[pk]+3,I[pk]+2,f"Peak: {I[pk]:.1f}%",color=col,fontsize=7.5)
        ax.set_title(lbl,color=C["fg"],fontsize=9,pad=4)
        ax.set_xlabel("Days",fontsize=8); ax.set_ylabel("Nodes (%)",fontsize=8)
        ax.set_xlim(0,120); ax.set_ylim(0,102)
        ax.legend(fontsize=7,loc="upper right",facecolor=C["bg"],edgecolor="#30363D")
        ax.grid(True,alpha=0.25)
    plt.suptitle(f"SIR-PACS Adversarial Propagation  [Day {day:.0f}/120]",
                 color=C["fg"],fontsize=10,fontweight="bold")
    plt.tight_layout(pad=0.4)
    frames.append(frame(fig,sz))
gif(frames,f"{OUT}/sir_propagation.gif",fps=14)

# ── GIF 4: QPUF Defence ────────────────────────────────────────────────────
print("4/6 QPUF Defence...")
frames=[]; sz=FIXED_W["double"]
for f in range(42):
    t=f/42
    fig,ax=plt.subplots(figsize=(9,4),facecolor=C["bg"])
    ax.set_facecolor(C["bg"]); ax.set_xlim(0,10); ax.set_ylim(0,4.5); ax.axis("off")
    ax.set_title("QPUF-DICOM Integrity Protocol",color=C["fg"],fontsize=11,fontweight="bold",pad=5)

    def box(x,y,w,h,lbl,sub,col,a=1.0):
        ax.add_patch(mpatches.FancyBboxPatch((x-w/2,y-h/2),w,h,
            boxstyle="round,pad=0.08",fc=col,alpha=a*0.85,ec="white",lw=0.8))
        ax.text(x,y+0.08,lbl,ha="center",va="center",fontsize=9,color="white",fontweight="bold",alpha=a)
        ax.text(x,y-0.22,sub,ha="center",va="center",fontsize=6.5,color="white",alpha=a*0.85)

    box(1.2,3.2,1.6,0.9,"CT Scanner","Acquisition",C["blue"])
    box(5.0,3.2,1.6,0.9,"PACS Server","Archive",C["purple"])
    box(8.8,3.2,1.6,0.9,"AI Inference","Diagnostic",C["teal"])
    box(5.0,1.2,1.6,0.9,"QPUF-CA","Cert Authority",C["orange"])

    p1=min(1.0,t/0.35)
    if t<0.45:
        ax.annotate("",xy=(4.2,3.2),xytext=(2.0,3.2),
            arrowprops=dict(arrowstyle="-|>",color=C["blue"],lw=2))
        px=2.0+p1*2.2
        ax.plot(px,3.2,"s",color=C["blue"],ms=11,alpha=0.9)
        ax.text(px,3.58,"DICOM\n+QPUF",ha="center",fontsize=6.5,color=C["blue"])
        ax.text(5,4.3,f"① Sign DICOM with QPUF challenge-response  [{p1*100:.0f}%]",
                ha="center",color=C["blue"],fontsize=8.5)
    if 0.35<=t<0.7:
        p2=min(1.0,(t-0.35)/0.3)
        ax.annotate("",xy=(5.0,1.65),xytext=(5.0,2.75),
            arrowprops=dict(arrowstyle="-|>",color=C["orange"],lw=2))
        bits="".join(str(rng.randint(0,2)) for _ in range(12))
        bhat="".join(str(int(b)^(rng.rand()<0.08)) for b in bits)
        dh=sum(a!=b for a,b in zip(bits,bhat))
        ax.text(5.0,0.35,f"r:    {bits}\nr̂:   {bhat}\nd_H={dh} ≤ τ=3  {'✓' if dh<=3 else '✗'}",
                ha="center",fontsize=6.5,color=C["teal"],fontfamily="monospace",alpha=p2)
        ax.text(5,4.3,f"② PACS queries CA for expected response r̂  [{p2*100:.0f}%]",
                ha="center",color=C["orange"],fontsize=8.5)
    if t>=0.65:
        p3=min(1.0,(t-0.65)/0.35)
        ax.annotate("",xy=(8.0,3.2),xytext=(5.8,3.2),
            arrowprops=dict(arrowstyle="-|>",color=C["green"],lw=2.5))
        ax.plot(5.8+p3*2.2,3.2,"D",color=C["green"],ms=11,alpha=0.9)
        ax.text(5,4.3,f"③ AUTHENTIC — forward to AI  [{p3*100:.0f}%]",
                ha="center",color=C["green"],fontsize=8.5,fontweight="bold")
    frames.append(frame(fig,sz))
gif(frames,f"{OUT}/qpuf_defence.gif",fps=13)

# ── GIF 5: ROC Animation ─────────────────────────────────────────────────
print("5/6 ROC Curve...")
frames=[]; sz=FIXED_W["square"]
roc_data=[
    ("QPUF (AUC=0.994)",[0,0.001,0.003,0.008,0.02,0.05,0.1,0.2,0.5,1.0],
                         [0,0.721,0.856,0.924,0.962,0.981,0.991,0.997,0.999,1.0],C["blue"]),
    ("Hash (AUC=0.941)", [0,0.01,0.03,0.07,0.14,0.25,0.4,0.6,0.8,1.0],
                         [0,0.45,0.61,0.73,0.82,0.88,0.93,0.97,0.99,1.0],C["orange"]),
    ("CNN (AUC=0.912)",  [0,0.02,0.05,0.10,0.18,0.30,0.48,0.65,0.82,1.0],
                         [0,0.38,0.55,0.68,0.77,0.84,0.91,0.95,0.98,1.0],C["green"]),
]
for f in range(38):
    t=f/38
    fig=plt.figure(figsize=(5.8,5.4),facecolor=C["bg"])
    ax=fig.add_subplot(111); ax.set_facecolor(C["bg"])
    ax.plot([0,1],[0,1],"--",color="#555",lw=1.2,alpha=0.5)
    ax.set_xlabel("False Positive Rate",fontsize=10); ax.set_ylabel("True Positive Rate",fontsize=10)
    ax.set_title("QPUF vs Classical — ROC Curves",color=C["fg"],fontsize=10,fontweight="bold")
    ax.set_xlim(-0.01,1.01); ax.set_ylim(-0.01,1.01); ax.grid(True,alpha=0.25)
    for i,(lbl,fpr,tpr,col) in enumerate(roc_data):
        d=i*0.25; p=min(1.0,max(0.0,(t-d)*2.5)); n=max(2,int(p*len(fpr)))
        ax.plot(fpr[:n],tpr[:n],"o-",color=col,lw=2.2,markersize=4,label=lbl,alpha=0.9)
        ax.fill_between(fpr[:n],0,tpr[:n],alpha=0.08,color=col)
    ax.legend(fontsize=8,loc="lower right",facecolor=C["bg"],edgecolor="#30363D")
    frames.append(frame(fig,sz))
gif(frames,f"{OUT}/roc_animation.gif",fps=12)

# ── GIF 6: Epidemic Network ───────────────────────────────────────────────
print("6/6 Epidemic Network...")
frames=[]; sz=FIXED_W["net"]
Nn=30
hub_x,hub_y=0.5,0.5
angles=np.linspace(0,2*np.pi,Nn-1,endpoint=False)
nx=np.concatenate([[hub_x],0.5+0.38*np.cos(angles)])
ny=np.concatenate([[hub_y],0.5+0.38*np.sin(angles)])
t_sim=np.linspace(0,80,160)
sol2=odeint(sir,[Nn-2,2,0],t_sim,args=(0.35,0.05))
S2,I2,R2=sol2[:,0]/Nn,sol2[:,1]/Nn,sol2[:,2]/Nn
rng2=np.random.RandomState(5)

for f in range(52):
    ti=int(f/52*len(t_sim))
    s,iv,r=S2[ti],I2[ti],R2[ti]
    fig,axes=plt.subplots(1,2,figsize=(9.6,4.4),facecolor=C["bg"])
    fig.patch.set_facecolor(C["bg"])
    ax0=axes[0]; ax0.set_facecolor(C["bg"]); ax0.set_xlim(-0.05,1.05); ax0.set_ylim(-0.05,1.05); ax0.axis("off")
    ax0.set_title("PACS Network",color=C["fg"],fontsize=10,fontweight="bold",pad=4)
    for i in range(1,Nn): ax0.plot([hub_x,nx[i]],[hub_y,ny[i]],"-",color="#1E3A5F",lw=0.7,alpha=0.45)
    ni,nr=int(iv*Nn),int(r*Nn)
    states=(["I"]*ni+["R"]*nr+["S"]*(Nn-ni-nr)); rng2.shuffle(states)
    sc={"S":C["blue"],"I":C["red"],"R":C["green"]}
    for i,(xi,yi,st) in enumerate(zip(nx,ny,states)):
        ax0.scatter(xi,yi,s=220 if i==0 else 90,c=sc[st],zorder=4,edgecolors="white",linewidths=0.6,alpha=0.9)
    for st,col,lbl in [("S",C["blue"],f"Susceptible ({int(s*100)}%)"),
                        ("I",C["red"], f"Infected ({int(iv*100)}%)"),
                        ("R",C["green"],f"Recovered ({int(r*100)}%)")]:
        ax0.scatter([],[],c=col,s=70,label=lbl)
    ax0.legend(fontsize=8,loc="lower left",facecolor=C["bg"],edgecolor="#30363D")
    ax0.text(0.5,-0.03,f"Day {t_sim[ti]:.0f} / 80",ha="center",color=C["fg"],fontsize=9)

    ax1=axes[1]; ax1.set_facecolor(C["bg"])
    ax1.plot(t_sim[:ti],S2[:ti]*100,"-",color=C["blue"],lw=2,label="S")
    ax1.plot(t_sim[:ti],I2[:ti]*100,"--",color=C["red"],lw=2.5,label="I")
    ax1.plot(t_sim[:ti],R2[:ti]*100,":",color=C["green"],lw=2,label="R")
    if ti>0: ax1.plot(t_sim[ti-1],I2[ti-1]*100,"o",color=C["red"],ms=8)
    ax1.fill_between(t_sim[:ti],0,I2[:ti]*100,alpha=0.14,color=C["red"])
    ax1.set_xlim(0,80); ax1.set_ylim(0,102)
    ax1.set_xlabel("Days",fontsize=9); ax1.set_ylabel("Node Fraction (%)",fontsize=9)
    ax1.set_title("Epidemic Curve (R₀=7.0)",color=C["fg"],fontsize=10,fontweight="bold",pad=4)
    ax1.legend(fontsize=8,loc="upper right",facecolor=C["bg"],edgecolor="#30363D")
    ax1.grid(True,alpha=0.3)
    plt.tight_layout(pad=0.7)
    frames.append(frame(fig,sz))
gif(frames,f"{OUT}/epidemic_network.gif",fps=13)

print("\n✅ All GIFs complete:")
for fn in sorted(os.listdir(OUT)):
    if fn.endswith(".gif"):
        kb=os.path.getsize(f"{OUT}/{fn}")//1024
        print(f"   {fn:35s} {kb:5d} KB")
