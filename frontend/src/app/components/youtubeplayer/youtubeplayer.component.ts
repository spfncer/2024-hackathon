import { Component } from '@angular/core';
import { YouTubePlayer } from '@angular/youtube-player';

@Component({
  selector: 'youtube-player-example',
  template: '<youtube-player [videoId]="videoId"></youtube-player>',
  standalone: true,
  imports: [YouTubePlayer]
})
export class YoutubePlayerExample {
  videoId: string = '05Y4F5efN38'; // Replace with your actual video ID
}