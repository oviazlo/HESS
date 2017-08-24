from __future__ import print_function
import ROOT
from array import array
import sys
import math

from ROOT import TCanvas, TGraphAsymmErrors, TLegend, TF1, TFile
from ROOT import gROOT

#  DM_mass = 50000
DM_mass = 48800

def b1(M):
        return 9.29*math.pow(M,-0.0139)
def c1(M):
	return 0.743*math.pow(M,0.0331)
def d1(M):
	return 0.265*math.pow(M,-0.0137)
def p(M):
	return 100000*math.pow(M,-1.13) + 285*math.pow(M,0.0794)
def j(M):
	return 0.943*math.pow(M,0.00852)

def x15dNdx(x,par):
	M = par[0]
	x0 = x[0]/M
	if x0>0.99:
		return 0.0
	if x0<0.001:
		return 0.0
	a1 = 25.8
	n1 = 0.51
	q = 3.0
	return a1 * math.exp( -b1(M)*math.pow(x0,n1) - c1(M)/math.pow(x0,d1(M)) ) * math.pow(math.log( p(M)*(j(M)-x0) )/math.log(p(M)),q)

def bkgFunc(x,par):
	par0 = 5.18*0.0001
	par1 = 2.8
	if x[0]<0.001:
		return 0.0
	return x[0]*x[0]*par0*par0*math.pow(x[0],-par1)

def sigFunc(x,par):
	A = 4.98*0.0000001
	#  return A*A*x15dNdx(x,par)*x15dNdx(x,par)*math.pow(x[0],1)
	if x[0]<0.001:
		return 0.0
	return A*A*x15dNdx(x,par)*math.pow(x[0]*par[0],0.5)

def sigAndBkg(x,par):
	return bkgFunc(x,par) + sigFunc(x,par)


#  bkgFunc = TF1("bkg","x*x*[0]*[0]*pow(x,-[1])",0,70000)
#  bkgFunc.SetParameter(0,5.18*0.0001)
#  bkgFunc.SetParameter(1,2.8)

########################################

def readDataIntoGraph():
	f=open('HESSj1745_290.dat',"r")
	lines=f.readlines()
	x, y, yHigh, yLow = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
	#  yScale = 10e12
	yScale = 1
	xScale = 1000
	for iLine in lines:
		if iLine.isspace() == True or iLine[0] == '#':
			continue
		tmpList = iLine.split()
		tmpX = xScale*float(tmpList[0])*float(tmpList[0])
		x.append(xScale*float(tmpList[0]))
		y.append(yScale*float(tmpList[1])*tmpX)
		yLow.append(yScale*(float(tmpList[1])-float(tmpList[2]))*tmpX)
		yHigh.append(yScale*(float(tmpList[3])-float(tmpList[1]))*tmpX)
	f.close()
	listOfZeros = array("d", [0] * len(x))
	gr = TGraphAsymmErrors(len(x),x,y,listOfZeros,listOfZeros,yLow,yHigh);
	#  gr.SetLineColor( color )
	gr.SetLineWidth( 2 )
	#  gr.SetMarkerColor( color )
	gr.SetMarkerStyle( 21 )
	gr.GetXaxis().SetTitle( 'Energy [GeV]' )
	gr.GetYaxis().SetTitle( 'E^{2} x Flux [GeV cm^{-2}s^{-1}]' )
	gr.SetTitle('')
	return gr

########################################

can1 = TCanvas( 'can1', 'A Simple Graph Example', 10, 10, 1810/2, 1210/2 )
can1.SetGrid()
can1.GetFrame().SetFillColor( 21 )
can1.GetFrame().SetBorderSize( 12 )
can1.Modified()
can1.Update()
can1.SetLogy()
can1.SetLogx()
#  can1.Divide(2,1)

leg = TLegend(0.55, 0.78, 0.75, 0.88)
leg.SetBorderSize(0)
leg.SetTextSize(0.03)

#  can1.cd(1)
dataGraph = readDataIntoGraph()
dataGraph.Draw("AP")
dataGraph.GetYaxis().SetRangeUser(5.0e-12,1.0e-06)
dataGraph.Draw("AP")

f_bkgFunc = TF1("bkg",bkgFunc,0,70000,1)
f_bkgFunc.SetParameter(0,DM_mass) # 50 TeV
f_bkgFunc.Draw("same")

f_sigFunc = TF1( "signalFunc", sigFunc,0,70000,1)
f_sigFunc.SetParameter(0,DM_mass) # 50 TeV
f_sigFunc.SetLineColor(4)
#  print (sigFunc.Eval(0.0001))
f_sigFunc.Draw("same")

f_sigAndBkgFunc = TF1("signalAndBkg",sigAndBkg,0,70000,1)
f_sigAndBkgFunc.SetParameter(0,DM_mass) # 50 TeV
f_sigAndBkgFunc.SetLineColor(3)
f_sigAndBkgFunc.Draw("same")

leg.AddEntry(dataGraph, 'exp. data', "lp");
leg.AddEntry(f_bkgFunc, 'background', "l");
leg.AddEntry(f_sigFunc, 'signal', "l");
leg.AddEntry(f_sigAndBkgFunc, 'signal fit + background', "l");
leg.Draw("same")
can1.SaveAs('test.png')
can1.SaveAs('test.root')

outFile = TFile ("outFile.root","RECREATE")
outFile.cd()
dataGraph.Write()

