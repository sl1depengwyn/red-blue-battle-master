import openSocket from 'socket.io-client';
const  socket = openSocket('192.168.99.100:8888');
function subscribeToTimer(cb) {
  socket.on('timer', timestamp => cb(null, timestamp));
  socket.emit('subscribeToTimer', 1000);
}
export { subscribeToTimer };