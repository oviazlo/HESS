from __future__ import print_function
import ROOT
from array import array
import sys
import math

from ROOT import TCanvas, TGraphAsymmErrors, TLegend, TF1, TFile
from ROOT import gROOT

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
	print (yHigh)
	print (y)
	print (yLow)
	f.close()
	listOfZeros = array("d", [0] * len(x))
	gr = TGraphAsymmErrors(len(x),x,y,listOfZeros,listOfZeros,yLow,yHigh);
	#  gr.SetLineColor( color )
	gr.SetLineWidth( 2 )
	#  gr.SetMarkerColor( color )
	gr.SetMarkerStyle( 21 )
	gr.GetXaxis().SetTitle( 'Energy [GeV]' )
	gr.GetYaxis().SetTitle( 'dN/dE [cm^{-2}s^{-1}GeV^{-1}]' )
	gr.SetTitle('')
	return gr

########################################

c1 = TCanvas( 'c1', 'A Simple Graph Example', 200, 10, 600, 500 )
c1.SetGrid()
c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderSize( 12 )
c1.Modified()
c1.Update()
c1.SetLogy()
c1.SetLogx()
#  c1.Divide(2,1)

leg = TLegend(0.7, 0.84, 0.9, 0.96)
leg.SetBorderSize(0)
leg.SetTextSize(0.03)

#  c1.cd(1)
dataGraph = readDataIntoGraph()
dataGraph.Draw("AP")
dataGraph.GetYaxis().SetRangeUser(5.0e-12,1.0e-08)
dataGraph.Draw("AP")

bkgFunc = TF1("bkg","x*x*[0]*[0]*pow(x,-[1])",0,70000)
bkgFunc.SetParameter(0,5.18*0.0001)
bkgFunc.SetParameter(1,2.8)
bkgFunc.Draw("same")

sigAndBkgFunc = TF1("signalAndBkg"," bkg + [0]*exp(-0.5*((x-48.8)/[1])**2)",0,70000)
sigAndBkgFunc.SetLineColor(3)
sigAndBkgFunc.SetParameter(0,10e-16)
sigAndBkgFunc.SetParameter(1,5)
#  dataGraph.Fit(sigAndBkgFunc,"R")
sigAndBkgFunc.Draw("same")

leg.AddEntry(dataGraph, 'exp. data', "lp");
leg.AddEntry(bkgFunc, 'background', "l");
leg.AddEntry(sigAndBkgFunc, 'signal fit + background', "l");
leg.Draw("same")
c1.SaveAs('test.png')
c1.SaveAs('test.root')

outFile = TFile ("outFile.root","RECREATE")
outFile.cd()
dataGraph.Write()

