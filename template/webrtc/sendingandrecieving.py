class SignalingChannel {
  constructor(remoteClientId) {
    this.remoteClientId = Username;
    const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const wsUrl = `${wsScheme}://${window.location.host}/chat/${Username}/${recipient}/`;

    this.socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.onMessage(message);
    };

    this.socket.onopen = () => {
      console.log('WebSocket connection opened');
    };

    this.socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  onMessage(message) {
    const event = new CustomEvent('message', { detail: message });
    document.dispatchEvent(event);
  }

  send(message) {
    this.socket.send(JSON.stringify(message));
  }
}

// Usage example (replace with your authentication logic)
async function handleCall(isInitiator, token) {
  const configuration = { iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] };
  const peerConnection = new RTCPeerConnection(configuration);

  signalingChannel.addEventListener('message', async (event) => {
    const message = event.detail;

    if (message.offer) {
      const remoteDesc = new RTCSessionDescription(message.offer);
      await peerConnection.setRemoteDescription(remoteDesc);
      const answer = await peerConnection.createAnswer();
      await peerConnection.setLocalDescription(answer);
      signalingChannel.send({ answer: answer, token: token });
    } else if (message.iceCandidate) {
      try {
        await peerConnection.addIceCandidate(message.iceCandidate);
      } catch (e) {
        console.error('Error adding received ice candidate', e);
      }
    }
  });

  peerConnection.onicecandidate = (event) => {
    if (event.candidate) {
      signalingChannel.send({ iceCandidate: event.candidate, token: token });
    }
  };

  // Sending Side Logic (if isInitiator)
  if (isInitiator) {
    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    signalingChannel.send({ offer: offer, token: token });
  }

  // Media Stream Management (if applicable)
  // ...
}

