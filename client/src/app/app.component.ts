import {Component} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {repeat, repeatWhen} from 'rxjs/operators';
import {interval} from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {

  constructor(private httpClient: HttpClient) {
  }

  title = 'client';

  backendaddress: string = 'http://89.27.83.105:5111';

  serverData: JSON;
  inputurlresponse: JSON;
  killmessage: JSON;
  employee: JSON;


  clickMessage = '';
  serverlist = [];
  serveritemlist = [];

  displaymessage: string;

  name: string;
  position: number;
  weight: number;
  symbol: string;


  inputurlval: string;
  inputkeywordval: string;
  inputfreqval: number;


  updatelock: number;


  ngOnInit() {
    this.updatelock = 0;
  }


  watchdog() {
    this.updatelock = 1;
    this.httpClient.get(this.backendaddress + '/watch').subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
      this.updatelock = 0;
    });

    if (this.updatelock === 1) {
      this.displaymessage = '';
    }
    let keys = Object.keys(this.serverData);
    // console.log(keys);
    // console.log(this.serverData[keys[0]]);
    for (let i = 0; i < keys.length; i++) {
      console.log(this.serverData[keys[i]]);
      this.serveritemlist[i] = this.serverData[keys[i]];
    }
    // console.log(this.dataSource[0].time);
    console.log(this.serveritemlist);


    this.serverlist = keys;


    console.log(this.serveritemlist);

    if (this.serveritemlist.length === 0) {
      this.displaymessage = 'empty';
    } else {
      this.displaymessage = 'watchdog ';
    }
  }

  inputurl() {
    console.log(this.inputurlval);
    // input control
    if (this.inputfreqval === undefined) {

      if (this.inputurlval === undefined) {
        this.displaymessage = 'the request URL is invalid';
        return;
      } else {
        if (this.inputkeywordval === undefined) {
          this.httpClient.get(this.backendaddress + '/input/' + this.inputurlval).subscribe(data => {
            this.inputurlresponse = data as JSON;
            console.log(this.inputurlresponse);
          });
          this.displaymessage = JSON.stringify(this.inputurlresponse);
        } else {
          this.httpClient.get(this.backendaddress + '/input/' + this.inputurlval + '&&' + this.inputkeywordval).subscribe(data => {
            this.inputurlresponse = data as JSON;
            console.log(this.inputurlresponse);
          });
          this.displaymessage = JSON.stringify(this.inputurlresponse);
        }

      }
    } else {
      if (this.inputurlval === undefined) {
        this.displaymessage = 'the request URL is invalid';
        return;
      } else {
        if (this.inputkeywordval === undefined) {
          this.httpClient.get(this.backendaddress + '/input/' + this.inputurlval + '/' + this.inputfreqval).subscribe(data => {
            this.inputurlresponse = data as JSON;
            console.log(this.inputurlresponse);
          });
          this.displaymessage = JSON.stringify(this.inputurlresponse);
        } else {
          this.httpClient.get(this.backendaddress + '/input/' + this.inputurlval + '&&' + this.inputkeywordval + '/' + this.inputfreqval).subscribe(data => {
            this.inputurlresponse = data as JSON;
            console.log(this.inputurlresponse);
          });
          this.displaymessage = JSON.stringify(this.inputurlresponse);
        }

      }
    }

  }


  killwatchdog() {
    this.httpClient.get(this.backendaddress + '/kill').subscribe(data => {
      this.killmessage = data as JSON;
      console.log(this.killmessage);
      this.serveritemlist = [];
    });
    this.displaymessage = null;
    this.displaymessage = JSON.stringify(this.killmessage);
    console.log(this.displaymessage);
  }


}





