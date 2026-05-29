import { useCallback, useEffect, useRef, useState } from 'react'
import './Captcha.css'

const CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'

function randomCode(len = 4): string {
  let s = ''
  for (let i = 0; i < len; i++) {
    s += CHARS[Math.floor(Math.random() * CHARS.length)]
  }
  return s
}

interface Props {
  onChange: (code: string) => void
}

export default function Captcha({ onChange }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [code, setCode] = useState('')

  const draw = useCallback(
    (value: string) => {
      const canvas = canvasRef.current
      if (!canvas) return
      const ctx = canvas.getContext('2d')
      if (!ctx) return

      const w = canvas.width
      const h = canvas.height
      ctx.clearRect(0, 0, w, h)
      ctx.fillStyle = '#f2f4f7'
      ctx.fillRect(0, 0, w, h)

      // interference lines
      for (let i = 0; i < 4; i++) {
        ctx.strokeStyle = `rgba(${rnd(120, 200)},${rnd(120, 200)},${rnd(
          120,
          200
        )},0.6)`
        ctx.beginPath()
        ctx.moveTo(rnd(0, w), rnd(0, h))
        ctx.lineTo(rnd(0, w), rnd(0, h))
        ctx.stroke()
      }

      // characters
      const colors = ['#00a847', '#3b7fd4', '#e3852b', '#7a52c9', '#d0455a']
      for (let i = 0; i < value.length; i++) {
        ctx.save()
        const x = 12 + i * 22
        const y = h / 2 + rnd(-3, 3)
        ctx.translate(x, y)
        ctx.rotate(((rnd(-22, 22) * Math.PI) / 180))
        ctx.font = `bold ${rnd(22, 26)}px Arial`
        ctx.fillStyle = colors[i % colors.length]
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(value[i], 0, 0)
        ctx.restore()
      }

      // dots
      for (let i = 0; i < 18; i++) {
        ctx.fillStyle = `rgba(${rnd(100, 200)},${rnd(100, 200)},${rnd(
          100,
          200
        )},0.7)`
        ctx.beginPath()
        ctx.arc(rnd(0, w), rnd(0, h), 1, 0, Math.PI * 2)
        ctx.fill()
      }
    },
    []
  )

  const refresh = useCallback(() => {
    const next = randomCode()
    setCode(next)
    onChange(next)
    draw(next)
  }, [draw, onChange])

  useEffect(() => {
    refresh()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <canvas
      ref={canvasRef}
      width={100}
      height={44}
      className="captcha-canvas"
      data-testid="captcha-image"
      title="点击刷新验证码"
      onClick={refresh}
      role="img"
      aria-label={`验证码 ${code}`}
    />
  )
}

function rnd(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min
}
