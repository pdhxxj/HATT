import wx
import threading
import time

import wx.lib.plot as plot
from Core.Info.performance import PerformanceInfo
from Core.Info.system import SystemInfo

threading._DummyThread._Thread__stop = lambda x: 42
p=PerformanceInfo()
s=SystemInfo()
########################################################################

########################################################################




########################################################################
class Prototype(wx.Frame):

      #----------------------------------------------------------------------
      def __init__(self, parent, title):
           wx.Frame.__init__(self, None, title="First Frame", size=(500,400))
           self.data = []
           self.UI()
           self.Centre()
           self.Show()

      #----------------------------------------------------------------------
      def UI(self):
           panel = wx.Panel(self,-1)
           vbox = wx.BoxSizer(wx.VERTICAL)
           hbox1 = wx.BoxSizer(wx.HORIZONTAL)
           l1 = wx.StaticText(panel, -1, "catchTime")
           hbox1.Add(l1, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
           self.t1 = wx.TextCtrl(panel)
           self.t1.SetMaxLength(2)
           hbox1.Add(self.t1,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
           vbox.Add(hbox1)
           hbox2 = wx.BoxSizer(wx.HORIZONTAL)
           l2 = wx.StaticText(panel, -1, "lautchTime")
           hbox2.Add(l2, 1, wx.ALIGN_LEFT|wx.ALL,5)
           self.t2 = wx.TextCtrl(panel)
           self.t2.SetMaxLength(5)
           hbox2.Add(self.t2,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
           vbox.Add(hbox2)
           hbox3 = wx.BoxSizer(wx.HORIZONTAL)
           self.t3 = wx.TextCtrl(panel,size = (200,100),style = wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_CENTER)
           hbox3.Add(self.t3,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
           vbox.Add(hbox3)
           hbox4 = wx.BoxSizer(wx.HORIZONTAL)
           self.btn1 = wx.Button(panel, label = "Start")
           self.btn2 = wx.Button(panel, label = "Clear")
           self.btn3 = wx.Button(panel, label = "Show")
           hbox4.Add(self.btn1,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
           self.btn1.Bind(wx.EVT_BUTTON, self.OnStart, self.btn1)
           hbox4.Add(self.btn2,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
           self.btn2.Bind(wx.EVT_BUTTON, self.OnClear, self.btn2)
           hbox4.Add(self.btn3,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
           self.btn3.Bind(wx.EVT_BUTTON, self.OnDraw, self.btn3)
           vbox.Add(hbox4)
           panel.SetSizer(vbox)
           self.Centre()
           self.Show()
      #----------------------------------------------------------------------

      def OnStart(self,event):
           #or isinstance(self.t1.GetValue().encode("utf-8"),str)
           if self.t1.GetValue().encode("utf-8") is '' :
               dlg=wx.MessageDialog(None,"Please Entry catchTime", "Error" ,wx.OK | wx.ICON_ERROR)
               if dlg.ShowModal()==wx.ID_OK:
                    self.t1.Clear()
               return
           if self.t2.GetValue().encode("utf-8") is '' :
               dlg=wx.MessageDialog(None,"Please Entry lauchTime", "Error" ,wx.OK | wx.ICON_ERROR)
               if dlg.ShowModal()==wx.ID_OK:
                    self.t2.Clear()

               return
           self.packageName="com.sfpay.mobile"
           #self.tmpTread()
           threading._start_new_thread(self.memTread,())
           #t = threading.Thread(target=self.tmpTread())
           #t.start()
           #print self.getAVG(self.t3.GetValue())
           #print self.getFlow()

      def  OnClear(self,event):
           self.t3.Clear()
           self.chargeDevice()

      def getFlow(self):
           if self.chargeDevice():
              raise Exception("device not found")
           sflow=p.getCurFlowFromProc(self.packageName)
           i=int(self.t2.GetValue())/int(self.t1.GetValue())
           while i>0:
               i=i-1
               time.sleep(int(self.t1.GetValue()))
           eflow=p.getCurFlowFromProc(self.packageName)
           flow=eflow-sflow
           return flow


      def memTread(self):
           i=int(self.t2.GetValue())/int(self.t1.GetValue())
           while i>0:
               i=i-1
               threading._start_new_thread(self.getMemData,())
               time.sleep(int(self.t1.GetValue()))

      def cpuTread(self):
           i=int(self.t2.GetValue())/int(self.t1.GetValue())
           while i>0:
               i=i-1
               threading._start_new_thread(self.getCpuData(),())
               time.sleep(int(self.t1.GetValue()))

      def chargeDevice(self):
          flag=False
          dlist=s.getDeviceIDlist()
          if len(dlist) ==0:
              flag=True
              return flag
          return flag



      def getMemData(self):
          tmp=p.getMemFromDump(self.packageName)
          if self.chargeDevice():
              raise Exception("device not found")
          if tmp == "error" :
              raise Exception(self.packageName+" is not found")
          else:
              self.data.append((self.getTextNo(),tmp))
              self.t3.AppendText(tmp+"\n")

      def getTextNo(self):
          tmp=self.t3.GetValue().split("\n")
          l=len(tmp)-1
          return l

      def getCpuData(self):
           tmp=p.getCpuFromDump(self.packageName)[0]
           if self.chargeDevice():
              raise Exception("device not found")
           if tmp.__contains__("process"):
               raise Exception(self.packageName+" is not found")
           else:
               self.data=tmp
               self.t3.AppendText(tmp+"\n")


      def getMemAvg(self,value):
           if value is None or "":
               raise Exception('value is none')
           else:
               tmp=value.split("\n")
               temp=tmp[:len(tmp)-1]
               sum=0
               for x in temp:
                    sum=sum+int(x)
               avg=sum/len(temp)
               return avg

      def getCpuAvg(self,value):
           if value is None or "":
               raise Exception('value is none')
           else:
               tmp=value.split("\n")
               temp=tmp[:len(tmp)-1]
               sum=0.0
               for x in temp:
                    j=x.split("%")[0]
                    sum=sum+float(j)
               avg=str(sum/len(temp))+"%"
               return avg

      def getDrawData(self,value):
            if value is None or "":
               raise Exception('value is none')
            else:
               tmp=value.split("\n")
               temp=tmp[:len(tmp)-1]
               l=[]
               n=0
               for x in temp:
                    m=str(n)+","+x
                    l.append(m)
                    n=n+1
               return l

      def getRealData(self,value):
          if value is None or "":
               raise Exception('value is none')
          else:
              return value

      def OnDraw(self, event):

           frm = wx.Frame(self, -1, 'demo', size=(600, 450))
           client = plot.PlotCanvas(frm)
           line = plot.PolyLine(self.data, colour='pink', width=5, \
                             legend='value')
           gc = plot.PlotGraphics([line], 'demo', 'X', 'Y')
           client.Draw(gc,yAxis=(0,200000))
           frm.Show()

#----------------------------------------------------------------------
app = wx.App(False)
desiredSize = wx.Size(400,300)
Prototype(None, title='')
app.MainLoop()