import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime

class Order:
    def __init__(self, symbol: str, order_type: str, quantity: float, 
                 price: float, timestamp: datetime):
        self.symbol = symbol
        self.order_type = order_type  # 'buy' or 'sell'
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp  # Already in Unix milliseconds
        self.status = 'pending'  # pending, filled, cancelled
        self.filled_price = None
        self.filled_quantity = 0

class OrderManager:
    def __init__(self):
        self.orders: List[Order] = []
        self.positions: Dict[str, float] = {}  # symbol -> quantity
        self.trade_history: List[Dict] = []
        
    def create_order(self, symbol: str, order_type: str, 
                    quantity: float, price: float, timestamp: Optional[int] = None) -> Order:
        """Create a new order"""
        if timestamp is None:
            timestamp = datetime.now()
        else:
            timestamp = datetime.fromtimestamp(timestamp / 1000)  # Convert Unix ms to datetime
            
        order = Order(
            symbol=symbol,
            order_type=order_type, 
            quantity=quantity,
            price=price,
            timestamp=timestamp
        )
        self.orders.append(order)
        return order
    
    def execute_order(self, order: Order, current_price: float) -> bool:
        """Execute an order at the current market price"""
        if order.status != 'pending':
            return False
            
        # Update order status
        order.status = 'filled'
        order.filled_price = current_price
        order.filled_quantity = order.quantity
        
        # Update positions
        if order.symbol not in self.positions:
            self.positions[order.symbol] = 0
            
        if order.order_type == 'buy':
            self.positions[order.symbol] += order.quantity
        else:  # sell
            self.positions[order.symbol] -= order.quantity
            
        # Record trade
        self.trade_history.append({
            'timestamp': order.timestamp,
            'symbol': order.symbol,
            'type': order.order_type,
            'quantity': order.quantity,
            'price': current_price,
            'value': order.quantity * current_price
        })
        
        return True
    
    def get_position(self, symbol: str) -> float:
        """Get current position for a symbol"""
        return self.positions.get(symbol, 0)
    
    def get_all_positions(self) -> Dict[str, float]:
        """Get all current positions"""
        return self.positions.copy()
    
    def get_trade_history(self) -> pd.DataFrame:
        """Get trade history as a DataFrame"""
        return pd.DataFrame(self.trade_history)
    
    def cancel_order(self, order: Order) -> bool:
        """Cancel a pending order"""
        if order.status == 'pending':
            order.status = 'cancelled'
            return True
        return False 