import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, LabelList } from 'recharts';

const RentVsBuyAnalysis = () => {
  const data = [
    {
      name: 'Rent',
      scenario: '3% Appreciation',
      appreciation: 0,
      equity: 0,
      investment: 135100,
      costs: -69600,
      net: 65500,
      details: 'Investment: $135k | Rent: -$70k'
    },
    {
      name: '3% Down',
      scenario: '3% Appreciation',
      appreciation: 57000,
      equity: 22020,
      investment: 129010,
      costs: -192400,
      net: 15630,
      details: 'Appreciation: $57k | Equity: $22k | Investment: $129k | Costs: -$192k (incl $30k closing)'
    },
    {
      name: '20% Down',
      scenario: '3% Appreciation',
      appreciation: 57000,
      equity: 18180,
      investment: 106400,
      costs: -150180,
      net: 31400,
      details: 'Appreciation: $57k | Equity: $18k | Investment: $106k | Costs: -$150k (incl $30k closing)'
    },
    {
      name: '100% Cash',
      scenario: '3% Appreciation',
      appreciation: 57000,
      equity: 0,
      investment: 0,
      costs: -55800,
      net: 1200,
      details: 'Appreciation: $57k | Costs: -$56k (incl $30k closing)'
    },
    {
      name: 'Rent',
      scenario: '7% Appreciation',
      appreciation: 0,
      equity: 0,
      investment: 135100,
      costs: -69600,
      net: 65500,
      details: 'Investment: $135k | Rent: -$70k'
    },
    {
      name: '3% Down',
      scenario: '7% Appreciation',
      appreciation: 133000,
      equity: 22020,
      investment: 129010,
      costs: -192400,
      net: 91630,
      details: 'Appreciation: $133k | Equity: $22k | Investment: $129k | Costs: -$192k (incl $30k closing)'
    },
    {
      name: '20% Down',
      scenario: '7% Appreciation',
      appreciation: 133000,
      equity: 18180,
      investment: 106400,
      costs: -150180,
      net: 107400,
      details: 'Appreciation: $133k | Equity: $18k | Investment: $106k | Costs: -$150k (incl $30k closing)'
    },
    {
      name: '100% Cash',
      scenario: '7% Appreciation',
      appreciation: 133000,
      equity: 0,
      investment: 0,
      costs: -55800,
      net: 77200,
      details: 'Appreciation: $133k | Costs: -$56k (incl $30k closing)'
    }
  ];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div style={{
          backgroundColor: 'white',
          border: '2px solid #374151',
          borderRadius: '8px',
          padding: '16px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
          minWidth: '280px'
        }}>
          <p style={{ fontWeight: 'bold', fontSize: '16px', marginBottom: '12px', color: '#111827' }}>
            {data.name} ({data.scenario})
          </p>
          <p style={{ fontSize: '14px', color: '#6b7280', marginBottom: '8px', lineHeight: '1.6' }}>
            {data.details}
          </p>
          <div style={{ borderTop: '1px solid #e5e7eb', paddingTop: '8px', marginTop: '8px' }}>
            <p style={{ fontWeight: 'bold', fontSize: '18px', color: data.net >= 0 ? '#059669' : '#dc2626' }}>
              Net Year 1: ${data.net.toLocaleString()}
            </p>
          </div>
        </div>
      );
    }
    return null;
  };

  const renderCustomLabel = (props) => {
    const { x, y, width, value, index } = props;
    const data = props.payload;
    return (
      <text
        x={x + width / 2}
        y={y - 10}
        fill="#111827"
        textAnchor="middle"
        fontWeight="600"
        fontSize="14"
      >
        ${(data.net / 1000).toFixed(0)}k
      </text>
    );
  };

  const data3pct = data.filter(d => d.scenario === '3% Appreciation');
  const data7pct = data.filter(d => d.scenario === '7% Appreciation');

  return (
    <div style={{
      width: '1600px',
      height: '900px',
      backgroundColor: '#FAFAFA',
      padding: '48px',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      boxSizing: 'border-box'
    }}>
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{
          fontSize: '36px',
          fontWeight: '700',
          margin: '0 0 12px 0',
          color: '#111827',
          letterSpacing: '-0.5px'
        }}>
          San Francisco: Rent vs. Buy Year 1 Net Position
        </h1>
        <p style={{
          fontSize: '18px',
          color: '#6b7280',
          margin: 0,
          lineHeight: '1.5'
        }}>
          $1.9M property • $5.8k/mo rent • 6% mortgage • Includes opportunity cost of 7% market returns on uninvested capital
        </p>
      </div>

      <div style={{ display: 'flex', gap: '32px', height: '640px' }}>
        <div style={{ flex: 1 }}>
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px', color: '#374151', textAlign: 'center' }}>
            3% Property Appreciation
          </h2>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={data3pct} margin={{ top: 40, right: 20, left: 40, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" vertical={false} />
              <XAxis
                dataKey="name"
                tick={{ fontSize: 13, fontWeight: 600, fill: '#374151' }}
                axisLine={{ stroke: '#9ca3af' }}
                angle={0}
              />
              <YAxis
                tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
                tick={{ fontSize: 12, fill: '#6b7280' }}
                axisLine={{ stroke: '#9ca3af' }}
                domain={[-200000, 200000]}
              />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={0} stroke="#374151" strokeWidth={2} />

              <Bar dataKey="appreciation" stackId="a" fill="#10b981" />
              <Bar dataKey="equity" stackId="a" fill="#34d399" />
              <Bar dataKey="investment" stackId="a" fill="#6ee7b7">
                <LabelList content={renderCustomLabel} position="top" />
              </Bar>
              <Bar dataKey="costs" stackId="a" fill="#ef4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div style={{ flex: 1 }}>
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px', color: '#374151', textAlign: 'center' }}>
            7% Property Appreciation
          </h2>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={data7pct} margin={{ top: 40, right: 20, left: 40, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" vertical={false} />
              <XAxis
                dataKey="name"
                tick={{ fontSize: 13, fontWeight: 600, fill: '#374151' }}
                axisLine={{ stroke: '#9ca3af' }}
                angle={0}
              />
              <YAxis
                tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
                tick={{ fontSize: 12, fill: '#6b7280' }}
                axisLine={{ stroke: '#9ca3af' }}
                domain={[-200000, 200000]}
              />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={0} stroke="#374151" strokeWidth={2} />

              <Bar dataKey="appreciation" stackId="a" fill="#10b981" />
              <Bar dataKey="equity" stackId="a" fill="#34d399" />
              <Bar dataKey="investment" stackId="a" fill="#6ee7b7">
                <LabelList content={renderCustomLabel} position="top" />
              </Bar>
              <Bar dataKey="costs" stackId="a" fill="#ef4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div style={{
        marginTop: '24px',
        padding: '20px 24px',
        backgroundColor: 'white',
        borderRadius: '8px',
        border: '1px solid #d1d5db',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div style={{ flex: 1 }}>
          <p style={{ fontSize: '14px', color: '#6b7280', margin: 0, lineHeight: '1.6' }}>
            <strong style={{ color: '#10b981' }}>Green:</strong> Appreciation + Equity + Investment returns •
            <strong style={{ color: '#ef4444', marginLeft: '16px' }}>Red:</strong> Annual costs (after tax) + $30k closing
          </p>
        </div>
        <div style={{
          padding: '8px 16px',
          backgroundColor: '#f3f4f6',
          borderRadius: '6px',
          fontSize: '13px',
          fontWeight: 600,
          color: '#374151'
        }}>
          Net values shown above bars
        </div>
      </div>
    </div>
  );
};

export default RentVsBuyAnalysis;
