/**
 * JanAI — Reusable WebRTC Audio DSP & Noise Suppression Helper
 *
 * Centralizes WebRTC microphone constraints across the frontend to enforce:
 *  - Dynamic Noise Suppression (filters background static, fans, traffic)
 *  - Acoustic Echo Cancellation (prevents AI speaker output from looping back)
 *  - Auto Gain Control (normalizes quiet vs loud speaking volumes)
 *  - 16kHz Mono Audio (reduces STT upload bandwidth by 50%)
 */

export const OPTIMAL_AUDIO_CONSTRAINTS = {
  echoCancellation: { ideal: true },
  noiseSuppression: { ideal: true },
  autoGainControl:  { ideal: true },
  channelCount:     { ideal: 1 },       // Mono audio stream
  sampleRate:       { ideal: 16000 },   // 16kHz optimal speech recognition frequency
}

/**
 * Requests microphone access with full WebRTC hardware DSP noise suppression enabled.
 * Falls back gracefully to standard mic input if the browser/device lacks DSP capability.
 *
 * @returns {Promise<MediaStream>} Cleaned WebRTC Audio Stream
 */
export async function getCleanMicrophoneStream() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    throw new Error('Microphone access is not supported by your browser.')
  }

  try {
    // Try with full DSP noise cancellation constraints
    return await navigator.mediaDevices.getUserMedia({
      audio: OPTIMAL_AUDIO_CONSTRAINTS,
    })
  } catch (err) {
    console.warn('Advanced audio constraints failed — falling back to standard microphone:', err)
    // Fallback: standard audio stream without specific constraints
    return await navigator.mediaDevices.getUserMedia({ audio: true })
  }
}
