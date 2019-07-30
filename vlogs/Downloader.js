/* @flow */

import React, { Component } from 'react';
/*

  This place might seem like jungle , but you can always come back here to know some BASIC stuff like encrypting a video or uploading
*/

import {
  View,
  Text,
  StyleSheet,
  Button,
} from 'react-native';
var RNFS = require('react-native-fs');
var forge = require('node-forge');
import { LogLevel, RNFFmpeg } from 'react-native-ffmpeg';
export default class Downloader extends Component {

  constructor(props){
   super(props);
   this.state = { downloaded: false}
 }
 componentDidMount(){
   var keyy = forge.random.getBytesSync(16);
   decoded_key = forge.util.bytesToHex(keyy);
   console.warn(decoded_key);
   this.setState({key: decoded_key}, function() {

   })
 }


  render() {
     download = (url, path) =>  {
      RNFS.downloadFile({fromUrl:'http://techslides.com/demos/sample-videos/small.mp4', toFile: RNFS.DocumentDirectoryPath + "/small.mp4"}).promise.then(res => {
          console.warn('downloaded file to ' + RNFS.DocumentDirectoryPath + "/small.mp4")

          this.setState({
            downloaded: true
          }, function(){

          });

    });
//-i small.mp4 -vcodec copy -acodec copy -encryption_scheme cenc-aes-ctr -encryption_key 76a6c65c5ea762046bd749a2e632ccbb -encryption_kid a7e61c373e219033c21091fa607bf3b8 small_enc.mp4
    }
    encrypt = () => {
      RNFFmpeg.execute('-i' + ' ' + RNFS.DocumentDirectoryPath + '/small.mp4 -vcodec copy -acodec copy -encryption_scheme cenc-aes-ctr '+'-encryption_key '+ this.state.key+' -encryption_kid a7e61c373e219033c21091fa607bf3b8 ' + RNFS.DocumentDirectoryPath + "/small_encrypted.mp4", ' ').then(result => console.log("FFmpeg process exited with rc " + result.rc));
      RNFFmpeg.getLastReturnCode().then(result => {
    console.warn("Last return code: " + result.lastRc);
});
    }

    listFiles = () => {
      RNFS.readDir(RNFS.DocumentDirectoryPath) // On Android, use "RNFS.DocumentDirectoryPath" (MainBundlePath is not defined)
  .then((result) => {
    console.warn('GOT RESULT', result);

    // stat the first file
    return Promise.all([RNFS.stat(result[0].path), result[0].path]);
  })
  .then((statResult) => {
    if (statResult[0].isFile()) {
      // if we have a file, read it
      return RNFS.readFile(statResult[1], 'utf8');
    }

    return 'no file';
  })
  .then((contents) => {
    // log the file contents
    console.log(contents);
  })
  .catch((err) => {
    console.log(err.message, err.code);
  });
    }





    var formData = new FormData();
    formData.append('file', {uri: "file://"+RNFS.DocumentDirectoryPath + "/small_encrypted.mp4", name: 'video.mp4', type: 'video/mp4'});

    return (
      <View style={styles.container}>
        <Text>I'm the Downloader component</Text>
        <Button
          onPress={download}
          title="Download"
          color="#841584"
          accessibilityLabel="Learn more about this purple button"
        />
        <Button
          onPress={encrypt}
          title="encrypt"
          color="#841584"
          accessibilityLabel="Learn more about this purple button"
        />
        <Button
          onPress={listFiles}
          title="list files"
          color="#841584"
          accessibilityLabel="Learn more about this purple button"
        />

        <Button
      onPress={() => fetch('http://192.168.0.105:8000/api/users/upload', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          "Content-Type": "multipart/form-data"
        },
          body: formData
        })
      }
      title={'Upload File'}
    />

      </View>
    );

  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
