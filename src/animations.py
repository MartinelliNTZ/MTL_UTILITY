"""
Animations module for MTL_UTIL UI components.

Provides reusable animation classes and functions for hover, click, and fade effects.
"""

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QParallelAnimationGroup, QPointF, QRect
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QPushButton, QToolButton, QTabBar, QListWidget, QListWidgetItem
from typing import Optional


class UIAnimations:
    """Collection of UI animation utilities."""

    @staticmethod
    def create_fade_animation(widget: QWidget, start_opacity: float = 0.0, end_opacity: float = 1.0,
                           duration: int = 300) -> QPropertyAnimation:
        """Create a fade in/out animation for a widget."""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        return animation

    @staticmethod
    def create_color_animation(widget: QWidget, property_name: bytes, start_color: QColor,
                             end_color: QColor, duration: int = 200) -> QPropertyAnimation:
        """Create a color transition animation."""
        animation = QPropertyAnimation(widget, property_name)
        animation.setDuration(duration)
        animation.setStartValue(start_color)
        animation.setEndValue(end_color)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        return animation

    @staticmethod
    def create_scale_animation(widget: QWidget, start_scale: float = 1.0, end_scale: float = 1.05,
                             duration: int = 150) -> QPropertyAnimation:
        """Create a scale animation for a widget."""
        # Note: For scale animation, we need to handle it differently as QWidget doesn't have scale property
        # We'll use a custom property or animate geometry
        animation = QPropertyAnimation(widget, b"geometry")
        current_rect = widget.geometry()
        center = current_rect.center()

        # Calculate scaled rectangle
        start_width = int(current_rect.width() * start_scale)
        start_height = int(current_rect.height() * start_scale)
        end_width = int(current_rect.width() * end_scale)
        end_height = int(current_rect.height() * end_scale)

        start_rect = QRect(center.x() - start_width//2, center.y() - start_height//2, start_width, start_height)
        end_rect = QRect(center.x() - end_width//2, center.y() - end_height//2, end_width, end_height)

        animation.setDuration(duration)
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        return animation

    @staticmethod
    def animate_hover_enter(widget: QWidget, duration: int = 300):
        """Animate widget on hover enter - smooth color and opacity transition."""
        if hasattr(widget, '_hover_animation') and widget._hover_animation.state() == QPropertyAnimation.State.Running:
            widget._hover_animation.stop()

        # For buttons and tool buttons, animate background color with fade
        if isinstance(widget, (QPushButton, QToolButton)):
            # Create parallel animation for color and opacity
            widget._hover_animation = QParallelAnimationGroup()
            
            # Color animation
            start_color = QColor("#0e639c")
            end_color = QColor("#1177bb")
            color_anim = UIAnimations.create_color_animation(
                widget, b"palette", start_color, end_color, duration
            )
            
            # Subtle scale animation
            scale_anim = UIAnimations.create_scale_animation(widget, 1.0, 1.02, duration//2)
            
            widget._hover_animation.addAnimation(color_anim)
            widget._hover_animation.addAnimation(scale_anim)
            widget._hover_animation.start()

    @staticmethod
    def animate_hover_leave(widget: QWidget, duration: int = 300):
        """Animate widget on hover leave - return to original state."""
        if hasattr(widget, '_hover_animation') and widget._hover_animation.state() == QPropertyAnimation.State.Running:
            widget._hover_animation.stop()

        if isinstance(widget, (QPushButton, QToolButton)):
            # Parallel animation for smooth return
            widget._hover_animation = QParallelAnimationGroup()
            
            start_color = QColor("#1177bb")
            end_color = QColor("#0e639c")
            color_anim = UIAnimations.create_color_animation(
                widget, b"palette", start_color, end_color, duration
            )
            
            scale_anim = UIAnimations.create_scale_animation(widget, 1.02, 1.0, duration//2)
            
            widget._hover_animation.addAnimation(color_anim)
            widget._hover_animation.addAnimation(scale_anim)
            widget._hover_animation.start()

    @staticmethod
    def animate_click(widget: QWidget):
        """Animate widget on click - quick scale down and back with color flash."""
        if hasattr(widget, '_click_animation') and widget._click_animation.state() == QPropertyAnimation.State.Running:
            return

        # Create more dramatic click animation
        scale_down = UIAnimations.create_scale_animation(widget, 1.0, 0.95, 80)
        scale_up = UIAnimations.create_scale_animation(widget, 0.95, 1.0, 120)

        # Color flash animation
        flash_color = QColor("#ffffff")
        original_color = QColor("#0e639c")
        color_flash = UIAnimations.create_color_animation(
            widget, b"palette", original_color, flash_color, 40
        )
        color_back = UIAnimations.create_color_animation(
            widget, b"palette", flash_color, original_color, 80
        )

        # Sequential animation group
        widget._click_animation = QSequentialAnimationGroup()
        
        # Parallel group for scale down and color flash
        down_group = QParallelAnimationGroup()
        down_group.addAnimation(scale_down)
        down_group.addAnimation(color_flash)
        
        widget._click_animation.addAnimation(down_group)
        widget._click_animation.addAnimation(color_back)
        widget._click_animation.addAnimation(scale_up)
        widget._click_animation.start()

    @staticmethod
    def animate_tab_hover_enter(tab_bar: QTabBar, tab_index: int):
        """Animate tab on hover enter - subtle background color change."""
        # For now, we'll use a simple stylesheet approach
        # In a more advanced implementation, we could animate the tab's background
        current_style = tab_bar.styleSheet()
        # This is a placeholder - real animation would require more complex implementation
        pass

    @staticmethod
    def animate_fade_in(widget: QWidget, duration: int = 500):
        """Fade in a widget when it appears."""
        widget.setWindowOpacity(0.0)
        animation = UIAnimations.create_fade_animation(widget, 0.0, 1.0, duration)
        animation.start()


class AnimatedButton(QPushButton):
    """Button with built-in hover and click animations."""

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)
        self._setup_animations()

    def _setup_animations(self):
        """Setup hover and click animations."""
        pass  # Animations handled in event methods

    def enterEvent(self, event):
        """Handle mouse enter for hover animation."""
        UIAnimations.animate_hover_enter(self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave for hover animation."""
        UIAnimations.animate_hover_leave(self)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press for click animation."""
        UIAnimations.animate_click(self)
        super().mousePressEvent(event)


class AnimatedToolButton(QToolButton):
    """Tool button with built-in hover and click animations."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        """Handle mouse enter for hover animation."""
        UIAnimations.animate_hover_enter(self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave for hover animation."""
        UIAnimations.animate_hover_leave(self)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press for click animation."""
        UIAnimations.animate_click(self)
        super().mousePressEvent(event)


class AnimatedTabBar(QTabBar):
    """Tab bar with hover animations."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Temporariamente desabilitado para testar
        # self.setMouseTracking(True)
        self._hovered_tab = -1

    def enterEvent(self, event):
        """Handle mouse enter."""
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave."""
        if self._hovered_tab >= 0:
            # Reset hover state
            self._hovered_tab = -1
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        """Track which tab is being hovered."""
        # Temporariamente desabilitado
        # tab_index = self.tabAt(event.position().toPoint())
        # if tab_index != self._hovered_tab:
        #     if self._hovered_tab >= 0:
        #         # Leave previous tab
        #         pass
        #     self._hovered_tab = tab_index
        #     if tab_index >= 0:
        #         # Enter new tab
        #         UIAnimations.animate_tab_hover_enter(self, tab_index)
        super().mouseMoveEvent(event)


class AnimatedListWidget(QListWidget):
    """List widget with hover animations for items."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self._hovered_item = None

    def enterEvent(self, event):
        """Handle mouse enter."""
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave - reset hover state."""
        if self._hovered_item is not None:
            # Animate item back to normal
            self._animate_item_leave(self._hovered_item)
            self._hovered_item = None
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        """Track which item is being hovered."""
        item = self.itemAt(event.position().toPoint())
        if item != self._hovered_item:
            if self._hovered_item is not None:
                # Leave previous item
                self._animate_item_leave(self._hovered_item)
            self._hovered_item = item
            if item is not None:
                # Enter new item
                self._animate_item_enter(item)
        super().mouseMoveEvent(event)

    def _animate_item_enter(self, item: QListWidgetItem):
        """Animate item on hover enter."""
        # For now, we'll use stylesheet changes as QListWidgetItem doesn't support direct animations
        # In a more advanced implementation, we could use custom painting
        pass

    def _animate_item_leave(self, item: QListWidgetItem):
        """Animate item on hover leave."""
